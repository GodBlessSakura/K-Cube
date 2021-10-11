from argon2 import PasswordHasher


class adminResources:
    def __init__(self, driver):
        self.driver = driver

    def list_all_except_credential(self):
        def _query(tx):
            query = (
                "MATCH p = (h)-[r]->(t)"
                "WHERE 'Credential' NOT IN labels(h) AND 'Credential' NOT IN labels(t)"
                "RETURN p;"
            )
            result = tx.run(query)
            try:
                return result
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
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
                    return record
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def listPermission(self):
        def _query(tx):
            query = " ".join(["MATCH (permission:Permission)", "RETURN permission"])
            result = tx.run(query)
            try:
                return [dict(record["permission"].items()) for record in result]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def listUserPermission(self):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (user:User)-[:PRIVILEGED_OF]->(permission:Permission)",
                    "RETURN user, collect(permission.role) as roles",
                ]
            )
            result = tx.run(query)
            try:
                return [
                    {"user": dict(record["user"].items()), "roles": record["roles"]}
                    for record in result
                ]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
