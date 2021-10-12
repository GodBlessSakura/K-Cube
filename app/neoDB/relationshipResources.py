from neo4j.exceptions import ConstraintError
from . import for_all_methods
from app import InvalidRequest
import re


def check_info(function):
    def wrapper(self, *args, **kwargs):
        if (
            "userId" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{3,100}$", kwargs["userId"]) == None
        ):
            raise InvalidRequest("Invalid userId pattern.")
        if (
            "name" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["name"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        return function(self, **kwargs)

    return wrapper


@for_all_methods(check_info)
class relationshipResources:
    def __init__(self, driver):
        self.driver = driver

    def createProposal(self, userId, name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (proposer:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canProposeRelationship: true})",
                    "MERGE (r:GraphRelationship{name:  $name})",
                    "MERGE (r)<-[:USER_PROPOSE]-(proposer);",
                ]
            )
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def removeProposal(self, userId, name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (:GraphRelationship{name:  $name})<-[proposal:USER_PROPOSE]-(:User{userId: $userId})",
                    "DELETE proposal",
                ]
            )
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def createApproval(self, userId, name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (approver:User{userId: $userId})-[:PRIVILEGED_OF]->(:Permission {canApproveRelationship: true})",
                    "MATCH (r:GraphRelationship{name: $name})",
                    "MERGE (r)<-[:USER_APPROVE]-(approver);",
                ]
            )
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def removeApproval(self, userId, name):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (:GraphRelationship{name:  $name})<-[approval:USER_APPROVE]-(:User{userId: $userId})",
                    "DELETE approval",
                ]
            )
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def listRelationship(self, userId):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (user:User{userId: $userId}) with user",
                    "MATCH (r:GraphRelationship)",
                    "OPTIONAL MATCH (proposers:User)-[:USER_PROPOSE]->(r)",
                    "OPTIONAL MATCH (r)<-[:USER_APPROVE]-(approvers:User)",
                    "RETURN r.name, count(distinct proposers) as nOfProposers, user IN collect(proposers) as amIProposing,",
                    "count(distinct approvers) as nOfApprovers, user IN collect(approvers) as amIApproving",
                ]
            )
            result = tx.run(query, userId=userId)
            try:
                return [
                    {
                        "name": record["r.name"],
                        "nOfProposers": record["nOfProposers"],
                        "amIProposing": record["amIProposing"],
                        "nOfApprovers": record["nOfApprovers"],
                        "amIApproving": record["amIApproving"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
