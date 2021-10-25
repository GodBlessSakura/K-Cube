from neo4j.exceptions import ConstraintError
from argon2 import PasswordHasher
from .resourcesGuard import for_all_methods, reject_invalid


@for_all_methods(reject_invalid)
class userResources:
    def __init__(self, driver):
        self.driver = driver

    def list_userId(self):
        def _query(tx):
            query = " ".join(["MATCH (user:User)", "RETURN user.userId;"])
            result = tx.run(query)
            try:
                rows = [record for record in result]
                return [row["user.userId"] for row in rows]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def is_userId_used(self, userId) -> bool:
        def _query(tx):
            query = " ".join(
                [
                    "OPTIONAL MATCH (n:User{userId: $userId})",
                    "RETURN n IS NOT NULL AS Predicate;",
                ]
            )
            result = tx.run(query, userId=userId)
            try:
                for record in result:
                    return record["Predicate"]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_user(self, userId, userName, email, password):
        ph = PasswordHasher()
        saltedHash = ph.hash(password)

        def _query(tx):
            query = " ".join(
                [
                    "MATCH (permission:Permission{role: 'restricted'})",
                    "CREATE (permission)<-[permission_grant:PRIVILEGED_OF]-(user:User {userId: $userId, userName: $userName, email: $email})",
                    "-[password_set:AUTHENTICATED_BY]->(:Credential {saltedHash: $saltedHash})",
                    "SET ",
                    "password_set.creationDate = timestamp(),",
                    "permission_grant.creationDate = timestamp()",
                    "RETURN user;",
                ]
            )
            result = tx.run(
                query,
                userId=userId,
                userName=userName,
                email=email,
                saltedHash=saltedHash,
            )
            try:
                rows = [record for record in result]
                return dict(rows[0]["user"].items())
            except ConstraintError as e:
                raise e
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def assign_role(
        self,
        userId,
        role,
    ):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH",
                    "(permission:Permission{role: $role}),",
                    "(user:User{userId: $userId})",
                    "MERGE (permission)<-[permission_grant:PRIVILEGED_OF]-(user)",
                    "ON CREATE",
                    "SET",
                    "permission_grant.creationDate = timestamp()",
                    "RETURN user, permission_grant, permission;",
                ]
            )
            try:
                result = tx.run(query, userId=userId, role=role)
                return [
                    {
                        "user": dict(record["user"].items()),
                        "permission_grant": dict(record["permission_grant"].items()),
                        "permission": dict(record["permission"].items()),
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def removeRole(
        self,
        userId,
        role,
    ):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH",
                    "(permission:Permission{role: $role})<-[permission_grant:PRIVILEGED_OF]-(user:User{userId: $userId})",
                    "DELETE permission_grant",
                    "RETURN user, permission_grant, permission;",
                ]
            )
            try:
                result = tx.run(query, userId=userId, role=role)
                return [
                    {
                        "user": dict(record["user"].items()),
                        "permission_grant": dict(record["permission_grant"].items()),
                        "permission": dict(record["permission"].items()),
                    }
                    for record in result
                ][0]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def authenticate_user(self, userId, password):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH (user:User{userId: $userId})-[:AUTHENTICATED_BY]->(password:Credential)",
                    "RETURN user, password.saltedHash as hash;",
                ]
            )
            result = tx.run(query, userId=userId)
            try:
                rows = [record for record in result]
                if len(rows) > 0:
                    saltedHash = rows[0]["hash"]
                    ph = PasswordHasher()
                    if ph.verify(saltedHash, password):
                        return dict(rows[0]["user"].items())
                    else:
                        return None
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_user_permission(self, userId):
        def _query(tx):
            query = " ".join(
                [
                    "MATCH    (:User{userId: $userId})-[:PRIVILEGED_OF]->(permissions:Permission)",
                    "RETURN permissions;",
                ]
            )
            result = tx.run(query, userId=userId)
            try:
                permission = dict()
                for row in [record for record in result]:
                    for key, value in row["permissions"].items():
                        if key not in permission:
                            permission[key] = value
                        else:
                            if not permission[key]:
                                permission[key] = value
                return permission
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
