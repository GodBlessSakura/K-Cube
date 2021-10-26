from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class APIDriver:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        queries = """CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT user_email_constraint IF NOT EXISTS ON (n:User) ASSERT n.email IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT draft_uid_constraint IF NOT EXISTS ON (n:Draft) ASSERT n.draftId IS UNIQUE;
CREATE CONSTRAINT course_uid_constraint IF NOT EXISTS ON (n:Course) ASSERT n.displayName IS UNIQUE;
CREATE CONSTRAINT GraphConcept_uid_constraint IF NOT EXISTS ON (n:GraphConcept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT GraphRelationship_uid_constraint IF NOT EXISTS ON (n:GraphRelationship) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;""".split(
            "\n"
        )
        queries.extend(
            [
                """MERGE (p:Permission {
    role: "admin"})
    SET
    p.canAssignRole = true,
    p.canCreateGraphConcept = true,
    p.canCreateCourse = true,
    p.canCreateJob = true,
    p.canCreateDraft = true,
    p.canProposeRelationship = true,
    p.canApproveRelationship = true,
    p.canOperateDraftForOthers = true,
    p.canUploadPhoto = true,
    p.canAccessAdminPanel = true,
    p.canOwnDraft = true;""",
                """MERGE (:Permission {
    role: "teacher",
    canCreateGraphConcept: true,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: true,
    canProposeRelationship: true,
    canApproveRelationship: false,
    canOperateDraftForOthers: false,
    canUploadPhoto: false,
    canOwnDraft: true
});""",
                """MERGE (:Permission {
    role: "restricted",
    canCreateGraphConcept: false,
    canCreateCourse: false,
    canCreateJob: false,
    canCreateDraft: false,
    canProposeRelationship: false,
    canApproveRelationship: false,
    canOperateDraftForOthers: false,
    canUploadPhoto: false,
    canOwnDraft: false
});""",
            ]
        )
        for query in queries:

            def _query(tx):

                result = tx.run(query)
                try:
                    return [record for record in result]
                except ServiceUnavailable as exception:
                    raise exception

            with self.driver.session() as session:
                session.write_transaction(_query)

        from .userResources import userResources

        self.user = userResources(driver=self.driver)

        from .courseResources import courseResources

        self.course = courseResources(driver=self.driver)

        from .adminResources import adminResources

        self.admin = adminResources(driver=self.driver)

        from .relationshipResources import relationshipResources

        self.relationship = relationshipResources(driver=self.driver)

        from .draftResources import draftResources

        self.draft = draftResources(driver=self.driver)

        from .tripleResources import tripleResources

        self.triple = tripleResources(driver=self.driver)

        from .graphResources import graphResources

        self.graph = graphResources(driver=self.driver)

        from .entityResources import entityResources

        self.entity = entityResources(driver=self.driver)

    def close(self):
        self.driver.close()
