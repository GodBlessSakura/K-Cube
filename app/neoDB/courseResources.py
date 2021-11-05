
from .resourcesGuard import for_all_methods, reject_invalid
import sys
from .cypher import cypher


@for_all_methods(reject_invalid)
class courseResources:
    def __init__(self, driver):
        self.driver = driver

    def create_course(self, displayName, name, imageURL):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                displayName=displayName,
                name=name,
                imageURL=imageURL,
            )
            try:
                return True
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_course(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
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

    def list_course_instructor(self, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode)
            try:
                return [
                    {
                        "userId": record["userId"],
                        "isAssigned": record["isAssigned"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def assign_course_instructor(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def unassign_course_instructor(self, courseCode, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, courseCode=courseCode, userId=userId)
            try:
                return
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def list_instructor_course(self, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
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
