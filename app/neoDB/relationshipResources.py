from neo4j.exceptions import ConstraintError
from .resourcesGuard import for_all_methods, reject_invalid
import sys
from .cypher import cypher


@for_all_methods(reject_invalid)
class relationshipResources:
    def __init__(self, driver):
        self.driver = driver

    def create_proposal(self, userId, name):
        fname = sys._getframe().f_code.co_name
        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_proposal(self, userId, name):
        fname = sys._getframe().f_code.co_name
        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_approval(self, userId, name):
        fname = sys._getframe().f_code.co_name
        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_approval(self, userId, name):
        fname = sys._getframe().f_code.co_name
        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId, name=name)
            try:
                return [record for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_relationship(self, userId):
        fname = sys._getframe().f_code.co_name
        def _query(tx):
            query = cypher[fname + ".cyp"]
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

    def list_approved_relationship(self):
        fname = sys._getframe().f_code.co_name
        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                return [record["r.name"] for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)