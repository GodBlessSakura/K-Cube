from neo4j import GraphDatabase
from .userResources import userResources
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class InvalidRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class APIDriver(userResources):
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        for query in """CREATE CONSTRAINT user_uid_constraint IF NOT EXISTS ON (n:User) ASSERT n.userId IS UNIQUE;
CREATE CONSTRAINT user_email_constraint IF NOT EXISTS ON (n:User) ASSERT n.email IS UNIQUE;
CREATE CONSTRAINT permission_uid_constraint IF NOT EXISTS ON (n:Permission) ASSERT n.role IS UNIQUE;
CREATE CONSTRAINT draft_uid_constraint IF NOT EXISTS ON (n:Draft) ASSERT n.draftId IS UNIQUE;
CREATE CONSTRAINT course_uid_constraint IF NOT EXISTS ON (n:Course) ASSERT n.displayName IS UNIQUE;
CREATE CONSTRAINT GraphConcept_uid_constraint IF NOT EXISTS ON (n:GraphConcept) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT GraphRelationship_uid_constraint IF NOT EXISTS ON (n:GraphRelationship) ASSERT n.name IS UNIQUE;
CREATE CONSTRAINT job_uid_constraint IF NOT EXISTS ON (n:Job) ASSERT n.jobId IS UNIQUE;
CREATE CONSTRAINT student_uid_constraint IF NOT EXISTS ON (n:Student) ASSERT n.studentId IS UNIQUE;""".split('\n'):
            def _query(tx):
                
                result = tx.run(query)
                try:
                    return [record for record in result]
                except ServiceUnavailable as exception:
                    raise exception

            with self.driver.session() as session:
                session.write_transaction(_query)
            self.user = userResources(self)

    def close(self):
        self.driver.close()
