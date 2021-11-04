from neo4j.exceptions import ConstraintError
from .resourcesGuard import for_all_methods, reject_invalid
import sys
from .cypher import cypher


@for_all_methods(reject_invalid)
class trunkResources:
    def __init__(self, driver):
        self.driver = driver

    def list_trunk_branch_edge(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [dict(record["edge"].items()) for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_trunk_branch_node(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [dict(record["node"].items()) for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)