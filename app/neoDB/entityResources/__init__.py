from neo4j.time import DateTime
from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


@for_all_methods(reject_invalid)
class entityDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_entity(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
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

    def get_user_course_entity(self, name, userId, courseCode):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, name=name, userId=userId, courseCode=courseCode)
            try:
                return [
                    {
                        "concept": dict(record["concept"].items()),
                        "data": [
                            dict(
                                {
                                    key: value
                                    if not isinstance(value, DateTime)
                                    else str(value.iso_format())
                                    for key, value in data.items()
                                }.items(),
                                labels=list(data.labels),
                                id=data.id,
                            )
                            for data in record["data"]
                        ],
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def entity_disambiguation(self, name, courseCode, newName, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, name=name, courseCode=courseCode, newName=newName, userId=userId
            )
            try:
                return [
                    {
                        "concept": dict(record["concept"].items()),
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
