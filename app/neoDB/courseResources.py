from neo4j.exceptions import ConstraintError
from . import for_all_methods
from app import InvalidRequest
import re

# this would force the function to ignore all positional argument
def check_user_info(function):
    def wrapper(self, *args, **kwargs):
        if (
            "displayName" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["displayName"]) == None
        ):
            raise InvalidRequest("Invalid course display name pattern")
        if (
            "name" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["name"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        return function(self, **kwargs)

    return wrapper


@for_all_methods(check_user_info)
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

    def listCourse(self):
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
