
from neo4j.time import DateTime
from .resourcesGuard import for_all_methods, reject_invalid
import sys
from .cypher import cypher


@for_all_methods(reject_invalid)
class workspaceResources:
    def __init__(self, driver):
        self.driver = driver
    def list_course_workspace_edge(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "property": {
                            key:value if not isinstance(value,DateTime) else str(value.iso_format())
                            for key, value in record["edges"].items()
                        },
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_course_workspace_node(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return [
                    {
                        "property": {
                            key:value if not isinstance(value,DateTime) else str(value.iso_format())
                            for key, value in record["nodes"].items()
                        }
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)