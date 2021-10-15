from neo4j.exceptions import ConstraintError
from argon2 import PasswordHasher
from . import for_all_methods
from app import InvalidRequest
import re

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
        return function(self, **kwargs)

    return wrapper


@for_all_methods(check_info)
class tripleResources:
    def __init__(self, driver):
        self.driver = driver
    
    def getTriples(self, draftId,userId):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (owner:User{userId: $userId})",
                    "WITH DISTINCT owner",
                    "MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(owner)",
                    "WITH DISTINCT draft",
                    "MATCH (h:GraphConcept)-[r:GRAPH_RELATIONSHIP{draftId: $draftId}]->(t:GraphConcept)",
                    "RETURN h.name, r.name, t.name;"
                ]
            )
            result = tx.run(query, draftId=draftId,userId=userId)
            try:
                return [{
                    "h_name":record["h.name"],
                    "r_name":record["r.name"],
                    "t_name":record["t.name"]
                    } for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def createtriple(self, draftId, userId,h_name,r_name,t_name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (user:User{userId: $userId})"
                    "-[:PRIVILEGED_OF]->(:Permission{canOwnDraft: true, canCreateGraphConcept: true})",
                    "WITH DISTINCT user",
                    "MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(user)",
                    "WITH DISTINCT draft",
                    "MATCH (approved_graph_relationship:GraphRelationship{name: $r_name})"
                    "<-[:USER_APPROVE]-(:User)-[:PRIVILEGED_OF]->(:Permission{canApproveRelationship: true})",
                    "WITH DISTINCT approved_graph_relationship, draft",
                    "MERGE (h:GraphConcept{name: $h_name})",
                    "MERGE (t:GraphConcept{name: $t_name})",
                    "MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_graph_relationship.name}]-> (t)",
                    "SET draft.lastModified = timestamp(),",
                    "r.creationDate = timestamp(),",
                    "r.draftId = draft.draftId",
                    "RETURN h.name, r.name, t.name;"
                ]
            )
            result = tx.run(query, draftId=draftId, userId=userId,h_name=h_name,r_name=r_name,t_name=t_name)
            try:
                row = [record for record in result][0]
                return {
                    "h_name":row["h.name"],
                    "r_name":row["r.name"],
                    "t_name":row["t.name"]
                    }
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
    
    def deletetriple(self, draftId,userId,h_name,r_name,t_name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(:User{userId: $userId})"
                    "-[:PRIVILEGED_OF]->(:Permission{canOwnDraft: true})",
                    "WITH DISTINCT draft",
                    "MATCH (draft:Draft{draftId: $draftId})",
                    "WITH DISTINCT draft",
                    "MATCH (h:GraphConcept{name: $h_name})",
                    "MATCH (t:GraphConcept{name: $t_name})",
                    "MATCH (h) -[r:GRAPH_RELATIONSHIP{name: $r_name, draftId : draft.draftId}]-> (t)",
                    "WITH h.name as h_name, r.name as r_name, t.name as t_name, r, draft",
                    "DELETE r",
                    "SET draft.lastModified = timestamp()",
                    "RETURN h_name, r_name, t_name;"
                ]
            )
            result = tx.run(query, draftId=draftId, userId = userId,h_name=h_name,r_name=r_name,t_name=t_name)
            try:
                row = [record for record in result][0]
                return {
                    "h_name":row["h_name"],
                    "r_name":row["r_name"],
                    "t_name":row["t_name"]
                    }
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)