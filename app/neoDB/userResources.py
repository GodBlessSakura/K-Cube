from neo4j.exceptions import ServiceUnavailable
from argon2 import PasswordHasher


class userResources:
    def __init__(self, base):
        self.base_resources = base

    def list_userId(self):
        def _query(tx):
            query = """MATCH (user:User)
RETURN user.userId;"""
            result = tx.run(query)
            try:
                return [record for record in result]
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)

    def is_userId_used(self, userId) -> bool:
        def _query(tx):
            query = """OPTIONAL MATCH (n:User{userId: $userId})
RETURN n IS NOT NULL AS Predicate;"""
            result = tx.run(query, userId=userId)
            try:
                for record in result:
                    return record["Predicate"]
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)

    def create_user(self, userId, userName, email, password):
        ph = PasswordHasher()
        saltedHash = ph.hash(password)

        def _query(tx):
            query = """MATCH (permission:Permission{role: "restricted"})
CREATE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user:User {userId: $userId, userName: $userName, email: $email})
-[password_set:AUTHENTICATED_BY]->(:Credential {saltedHash: $saltedHash, salt: $salt})
ON CREATE 
    SET 
        password_set.creationDate = timestamp(),
        permission_grant.creationDate = timestamp()
RETURN user;"""
            result = tx.run(
                query,
                userId=userId,
                userName=userName,
                email=email,
                saltedHash=saltedHash,
            )
            try:
                return [record for record in result][0]
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)

    def assign_role(
        self,
        userId,
        role,
    ):
        def _query(tx):
            query = """MATCH
    (permission:Permission{role: $role}),
    (user:User{userId: $useerId})
MERGE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user)
ON CREATE 
    SET 
        permission_grant.creationDate = timestamp()
RETURN user, permission_grant, permission;"""
            result = tx.run(query, userId=userId, role=role)
            try:
                return [record for record in result][0]
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)


    def authenticate_user(self, userId, password):
        def _query(tx):
            query = """MATCH (user:User{userId: $userId})-[:AUTHENTICATED_BY]->(password:Credential)
RETURN user, password.saltedHash as hash;"""
            result = tx.run(query, userId=userId)
            try:
                rows = [record for record in result]
                if len(rows) > 0:
                    saltedHash = rows[0]["hash"]
                    ph = PasswordHasher()
                    if ph.verify(saltedHash, password):
                        return rows[0]["user"]
                    else:
                        return None
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)


    def get_user_permission(self, userId):
        def _query(tx):
            query = """MATCH 
    (:User{userId: $userId})-[:PRIVILEGED_OF]->(permissions:Permission),
RETURN permissions;"""
            result = tx.run(query, userId=userId)
            try:
                permission = dict()
                for row in [record for record in result]:
                    for key in row['permissions']["properties"]:
                        if key not in permission:
                            permission[key] = row['permissions']["properties"][key]
                        else:
                            if not permission[key]:
                                permission[key] = row['permissions']["properties"][key]
                return permission
            except ServiceUnavailable as exception:
                raise exception

        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)
