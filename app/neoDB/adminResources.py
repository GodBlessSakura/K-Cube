from neo4j.exceptions import ServiceUnavailable
from argon2 import PasswordHasher


class adminResources:
    def __init__(self, base):
        self.base_resources = base

    def list_all_except_credential(self):
        def _query(tx):
            query = (
                "MATCH p = (h)-[r]->(t)"
                "WHERE 'Credential' NOT IN labels(h) AND 'Credential' NOT IN labels(t)"
                "RETURN p;"
            )
            result = tx.run(query)
            try:
                return [record for record in result]
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)

    def readOnly_query(self, query) -> bool:
        CUD_keywords = ["CREATE", "MERGE", "SET", "DELETE", "REMOVE"]
        CUD_keywords = [keyword.strip() for keyword in CUD_keywords]
        CUD_keywords = [keyword.upper() for keyword in CUD_keywords]
        for keyword in CUD_keywords:
            if keyword in query.upper():
                return None

        def _query(tx):
            result = tx.run(query)
            try:
                for record in result:
                    return record["Predicate"]
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)
