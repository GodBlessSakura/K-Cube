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
                        "id": record["edges"].id,
                        "type": record["edges"].type,
                        "start": record["edges"].start_node.id,
                        "end": record["edges"].end_node.id,
                        "property": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
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
                        "id": record["nodes"].id,
                        "canPatch": record["canPatch"],
                        "property": {
                            key: value
                            if not isinstance(value, DateTime)
                            else str(value.iso_format())
                            for key, value in record["nodes"].items()
                        },
                    }
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_workspace(self, deltaGraphId, tag, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, tag=tag, userId=userId)
            try:
                return [record for record in result][0]["deltaGraphId"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_repository(self, deltaGraphId, tag, userId, w_tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, deltaGraphId=deltaGraphId, tag=tag, userId=userId, w_tag=w_tag
            )
            try:
                return [record for record in result][0]["deltaGraphId"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_workspace(self, deltaGraphId, userId):
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
                        for key, value in record["workspace"].items()
                    }.items()
                    | record["course"].items()
                )
                for record in result
            ][0]

            try:
                return workspace
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_workspace_subject(self, deltaGraphId, userId):
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
                        for key, value in record["subject"].items()
                    }.items()
                    | {
                        "isPatchLeaf": record["isPatchLeaf"],
                        "isOwner": record["isOwner"],
                    }.items(),
                    labels=list(record["subject"].labels),
                    courseCode=record["courseCode"],
                )
                for record in result
            ][0]

            try:
                return workspace
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def commit_workspace_as_fork(self, deltaGraphId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId, tag=tag)
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def commit_workspace_as_patch(self, deltaGraphId, userId, tag):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId, tag=tag)
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["branch"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def sync_workspace(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, deltaGraphId=deltaGraphId, userId=userId)
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["workspace"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def checkout_workspace(self, deltaGraphId, userId, checkout):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query, deltaGraphId=deltaGraphId, userId=userId, checkout=checkout
            )
            try:
                return [
                    {
                        key: value
                        if not isinstance(value, DateTime)
                        else str(value.iso_format())
                        for key, value in record["workspace"].items()
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_from_import(self, deltaGraphId, triples, userId, tag):
        fname = sys._getframe().f_code.co_name
        print(triples)

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                triples=triples,
                userId=userId,
                tag=tag,
            )
            try:
                return [record for record in result][0]["deltaGraphId"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def delete_workspace(self, deltaGraphId, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                deltaGraphId=deltaGraphId,
                userId=userId,
            )
            try:
                return True
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
