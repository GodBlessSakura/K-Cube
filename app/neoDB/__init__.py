from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import sys
from .cypher import cypher


class APIDriver:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

        from .userResources import userResources

        self.user = userResources(driver=self.driver)

        from .courseResources import courseResources

        self.course = courseResources(driver=self.driver)

        from .adminResources import adminResources

        self.admin = adminResources(driver=self.driver)

        from .relationshipResources import relationshipResources

        self.relationship = relationshipResources(driver=self.driver)

        from .tripleResources import tripleResources

        self.triple = tripleResources(driver=self.driver)

        from .graphResources import graphResources

        self.graph = graphResources(driver=self.driver)

        from .entityResources import entityResources

        self.entity = entityResources(driver=self.driver)

        from .trunkResources import trunkResources

        self.trunk = trunkResources(driver=self.driver)

        from .branchResources import branchResources

        self.branch = branchResources(driver=self.driver)

        from .workspaceResources import workspaceResources

        self.workspace = workspaceResources(driver=self.driver)

    def close(self):
        self.driver.close()

    def init_neo4j(self):

        fname = sys._getframe().f_code.co_name
        query = cypher[fname + ".cyp"]
        queries = query.split(";")
        for query in queries:

            def _query(tx):
                result = tx.run(query)
                try:
                    return [record for record in result]
                except ServiceUnavailable as exception:
                    raise exception

            with self.driver.session() as session:
                session.write_transaction(_query)
