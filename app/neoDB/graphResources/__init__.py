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
class graphResources:
    def __init__(self, driver):
        self.driver = driver

    def get_graph(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            workspace = [
                dict(
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["graph"].items()
                    }.items()
                    | {
                        "isPatchLeaf": record["isPatchLeaf"],
                        "isOwner": record["isOwner"],
                    }.items()
                    | record["course"].items(),
                    labels=list(record["graph"].labels),
                )
                for record in result
            ][0]

            try:
                return workspace
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
