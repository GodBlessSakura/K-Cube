from ..resourcesGuard import for_all_methods, reject_invalid
import sys
from importlib import resources

cypher = {
    f: resources.read_text(__package__, f)
    for f in resources.contents(__package__)
    if resources.is_resource(__package__, f) and f.split(".")[-1] == "cyp"
}


@for_all_methods(reject_invalid)
class tripleResources:
    def __init__(self, driver):
        self.driver = driver

    def get_workspace_triple(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                return [
                    {
                        "h_name": record["h.name"],
                        "r_name": record["r.name"],
                        "t_name": record["t.name"],
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
