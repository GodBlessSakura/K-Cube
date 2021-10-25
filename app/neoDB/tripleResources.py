from neo4j.exceptions import ConstraintError
from argon2 import PasswordHasher
from .resourcesGuard import for_all_methods,  reject_invalid
from app import InvalidRequest
import re



@for_all_methods(reject_invalid)
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
                    "MERGE (h) -[r:GRAPH_RELATIONSHIP{name: approved_graph_relationship.name, draftId: draft.draftId}]-> (t)",
                    "SET draft.lastModified = timestamp(),",
                    "r.creationDate = timestamp()",
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

    def deleteUnreachable(self,draftId,userId):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (draft:Draft{draftId: $draftId})<-[:USER_OWN]-(:User{userId: $userId})"
                    "-[:PRIVILEGED_OF]->(:Permission{canOwnDraft: true})",
                    "WITH DISTINCT draft",
                    "MATCH (root:GraphConcept)<-[:COURSE_DESCRIBE]-(:Course)<-[:DRAFT_DESCRIBE]-(draft:Draft)",
                    "WITH draft, root",
                    "MATCH reachable=(root)-[:GRAPH_RELATIONSHIP*{draftId : draft.draftId}]-(:GraphConcept)",
                    "UNWIND relationships(reachable) AS reachable_relationships",
                    "WITH collect(id(reachable_relationships)) as reachable_id, draft",
                    "MATCH (h)-[r:GRAPH_RELATIONSHIP{draftId : draft.draftId}]->(t)",
                    "WHERE NOT id(r) IN reachable_id",
                    "WITH collect(h.name) as h_name, collect(r.name) as r_name, collect(t.name) as t_name, r, draft",
                    "DELETE r",
                    "SET draft.lastModified = timestamp()",
                    "RETURN h_name, r_name, t_name;"
                ]
            )
            result = tx.run(query, draftId=draftId, userId = userId)
            try:
                return [{
                    "h_name":record["h_name"],
                    "r_name":record["r_name"],
                    "t_name":record["t_name"]
                    } for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def aggregateTriple(self):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (selected_draft:Draft{status: 'published'})<-[:USER_OWN]-(owner:User)",
                    "WITH selected_draft.draftId as published_id, owner.userId as userId",
                    "WITH published_id, userId",
                    "MATCH (h:GraphConcept)-[r:GRAPH_RELATIONSHIP]->(t:GraphConcept)",
                    "WHERE r.draftId in published_id",
                    "RETURN h.name, r.name, t.name , count(distinct published_id) AS draftVote, count(distinct userId) AS userVote"
                ]
            )
            result = tx.run(query)
            try:
                return [{
                    "h_name":record["h.name"],
                    "r_name":record["r.name"],
                    "t_name":record["t.name"],
                    "draftVote": record["draftVote"],
                    "userVote": record["userVote"],
                    } for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)