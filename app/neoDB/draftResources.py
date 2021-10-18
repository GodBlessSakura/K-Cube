from neo4j.exceptions import ConstraintError
from . import for_all_methods
from app import InvalidRequest
import re

# this would force the function to ignore all positional argument
def check_info(function):
    def wrapper(self, *args, **kwargs):
        if (
            "courseCode" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["courseCode"]) == None
        ):
            raise InvalidRequest("Invalid course display name pattern")
        if (
            "draftName" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["draftName"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        if (
            "userId" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{3,100}$", kwargs["userId"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        if "status" in kwargs and kwargs["status"] not in ["published", "unpublished"]:
            raise InvalidRequest("Invalid name pattern.")
        return function(self, **kwargs)

    return wrapper


@for_all_methods(check_info)
class draftResources:
    def __init__(self, driver):
        self.driver = driver

    def getDraft(self, draftId, userId):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (owner:User{userId: $userId})",
                    "WITH DISTINCT owner",
                    "MATCH (courseConcept:GraphConcept)<-[:COURSE_DESCRIBE]-(course:Course)<-[:DRAFT_DESCRIBE]-"
                    "(draft:Draft{draftId: $draftId})<-[:USER_OWN]-(owner)",
                    "RETURN draft, courseConcept.name as root, course",
                ]
            )
            result = tx.run(query, draftId=draftId, userId=userId)
            try:
                row = [record for record in result][0]
                draft = dict(row["draft"].items())
                draft["root"] = row["root"]
                draft["course"] = dict(row["course"].items())
                return draft
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def setStatus(self, draftId, userId, status):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(owner:User{userId: $userId})"
                    "-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOwnDraft: true})",
                    "WITH DISTINCT draft",
                    "SET draft.status = $status",
                    "RETURN draft.status;",
                ]
            )
            result = tx.run(
                query,
                draftId=draftId,
                userId=userId,
                status=status,
            )
            try:
                return [record for record in result][0]["draft.status"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def createDraft(self, draftName, userId, name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (owner:User{userId: $userId})-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOwnDraft: true})"
                    "WITH DISTINCT owner",
                    # if user have multiple permission that canCreateDraft and canOwnDraft, two identical user would be returned
                    "MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept:GraphConcept{name: $name})",
                    "CREATE (owner)-[:USER_OWN]->(draft:Draft)-[:DRAFT_DESCRIBE]->(course)",
                    'SET draft.draftId = owner.userId + "." + replace(courseConcept.name," ", "_") + "." + replace($draftName," ", "_"),',
                    "draft.draftName = $draftName,",
                    "draft.creationDate = timestamp(),",
                    "draft.lastModified = timestamp(),",
                    "draft.status = 'unpublished'",
                    "RETURN draft;",
                ]
            )
            result = tx.run(
                query,
                draftName=draftName,
                userId=userId,
                name=name,
            )
            try:
                return dict([record for record in result][0]["draft"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def listDraft(self, userId, name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (:GraphConcept{name: $name})<-[:COURSE_DESCRIBE]-(:Course)"
                    "<-[:DRAFT_DESCRIBE]-(draft:Draft)<-[:USER_OWN]-(:User{userId: $userId})",
                    "RETURN draft",
                ]
            )
            result = tx.run(query, name=name, userId=userId)
            try:
                return [dict(record["draft"].items()) for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def cloneDraft(self, draftName, userId, name, draftId):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (owner:User{userId: $userId})-[:PRIVILEGED_OF]-(:Permission{canCreateDraft: true, canOwnDraft: true})"
                    "WITH DISTINCT owner",
                    # if user have multiple permission that canCreateDraft and canOwnDraft, two identical user would be returned
                    "MATCH (course:Course)-[:COURSE_DESCRIBE]->(root:GraphConcept{name: $name})",
                    "CREATE (owner)-[:USER_OWN]->(draft:Draft)-[:DRAFT_DESCRIBE]->(course)",
                    'SET draft.draftId = owner.userId + "." + replace(root.name," ", "_") + "." + replace($draftName," ", "_"),',
                    "draft.draftName = $draftName,",
                    "draft.creationDate = timestamp(),",
                    "draft.lastModified = timestamp(),",
                    "draft.status = 'unpublished'",
                    "WITH draft,root",
                    "MATCH (source:Draft{draftId: $draftId})-[:DRAFT_DESCRIBE]->()"
                    "-[:COURSE_DESCRIBE]->(source_root:GraphConcept)",
                    "WITH draft, source, source_root, root",
                    "MATCH (h:GraphConcept)-[source_r:GRAPH_RELATIONSHIP{draftId: source.draftId}]->(t:GraphConcept)",
                    "WITH draft, source, source_root, root, h, source_r, t",
                    "CALL{",
                    "WITH draft, source, source_root, root, h, source_r, t",
                    "WITH draft, source, source_root, root, h, source_r, t",
                    "WHERE h <> source_root AND t <> source_root",
                    "MERGE (h) -[r:GRAPH_RELATIONSHIP{name: source_r.name, draftId: draft.draftId}]-> (t)",
                    "ON CREATE SET",
                    "r.creationDate = timestamp()",
                    "RETURN NULL",
                    "UNION",
                    "WITH draft, source, source_root, root, h, source_r, t",
                    "WITH draft, source, source_root, root, h, source_r, t",
                    "WHERE h = source_root AND t <> root",
                    "MERGE (root) -[r:GRAPH_RELATIONSHIP{name: source_r.name, draftId: draft.draftId}]-> (t)",
                    "ON CREATE SET",
                    "r.creationDate = timestamp()",
                    "RETURN NULL",
                    "UNION",
                    "WITH draft, source, source_root, root, h, source_r, t",
                    "WITH draft, source, source_root, root, h, source_r, t",
                    "WHERE t = source_root AND h <> root",
                    "MERGE (h) -[r:GRAPH_RELATIONSHIP{name: source_r.name, draftId: draft.draftId}]-> (root)",
                    "ON CREATE SET",
                    "r.creationDate = timestamp()",
                    "RETURN NULL",
                    "}",
                    "RETURN draft;",
                ]
            )
            result = tx.run(
                query,
                draftName=draftName,
                userId=userId,
                name=name,
                draftId=draftId,
            )
            try:
                return dict([record for record in result][0]["draft"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
