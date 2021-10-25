from neo4j.exceptions import ConstraintError
from argon2 import PasswordHasher
from .resourcesGuard import for_all_methods, reject_invalid


@for_all_methods(reject_invalid)
class entityResources:
    def __init__(self, driver):
        self.driver = driver

    def getEntities(self):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (concept:GraphConcept)",
                    "OPTIONAL MATCH (course:Course)-[:COURSE_DESCRIBE]->(concept:GraphConcept)",
                    "RETURN course, concept",
                ]
            )
            result = tx.run(query)
            try:
                return [
                    {
                        "course": dict(record["course"].items())
                        if record["course"] is not None
                        else None,
                        "concept": dict(record["concept"].items()),
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
