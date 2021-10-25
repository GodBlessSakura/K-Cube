from neo4j.exceptions import ConstraintError
from .resourcesGuard import for_all_methods, reject_invalid


@for_all_methods(reject_invalid)
class courseResources:
    def __init__(self, driver):
        self.driver = driver

    def courseCreate(self, displayName, name, imageURL):
        def _query(tx):
            query = " ".join(
                [
                    "MERGE (courseConcept:GraphConcept{name: $name})",
                    "MERGE (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)",
                    "SET course.imageURL = $imageURL, course.displayName = $displayName",
                    "RETURN course, courseConcept",
                ]
            )
            result = tx.run(
                query,
                displayName=displayName,
                name=name,
                imageURL=imageURL,
            )
            try:
                return dict([record for record in result][0].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def courseList(self):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (course:Course)-[:COURSE_DESCRIBE]->(courseConcept)",
                    "RETURN course,courseConcept",
                ]
            )
            result = tx.run(query)
            try:
                return [
                    {
                        "course": dict(record["course"].items()),
                        "concept": dict(record["courseConcept"].items()),
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
