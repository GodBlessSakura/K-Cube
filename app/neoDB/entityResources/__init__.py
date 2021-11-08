
from argon2 import PasswordHasher
from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}



@for_all_methods(reject_invalid)
class entityResources:
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
