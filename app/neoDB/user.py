
from neo4j.exceptions import ServiceUnavailable
from argon2 import PasswordHasher
class userResources():
    def __init__(self, base):
        self.base_resources = base

    def list_userId(self):
        def _query(tx):
            query = ("""
MATCH (user:User)
RETURN user.userId;"""
            )
            result = tx.run(query )
            try:
                return result
            except ServiceUnavailable as exception:
                raise exception
        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)
    def check_used_userId(self,userId):
        def _query(tx):
            query = ("""
RETURN exists((:User{userId: $userId}));"""
            )
            result = tx.run(query )
            try:
                return result
            except ServiceUnavailable as exception:
                raise exception
        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query, userId = userId)

    def create_user(self, userId, userName, email, password):
        ph = PasswordHasher()
        saltedHash =  ph.hash("password")
        def _query(tx):
            query = ("""
MATCH (permission:Permission{role: "restricted"})
CREATE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user:User {userId: $userId, userName: $userName, email: $email})
-[password_set:WEB_IS_AUTHENTICATED_BY]->(:Credential {saltedHash: $saltedHash, salt: $salt})
ON CREATE 
    SET 
        password_set.creationDate = timestamp(),
        permission_grant.creationDate = timestamp()
RETURN user;"""
            )
            result = tx.run(query , userId = userId, userName = userName, email = email, saltedHash = saltedHash)
            try:
                return result[0]
            except ServiceUnavailable as exception:
                raise exception
        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)
    def assign_role(self, userId, role,):
        def _query(tx):
            query = ("""
MATCH
    (permission:Permission{role: $role}),
    (user:User{userId: $useerId})
MERGE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user)
ON CREATE 
    SET 
        permission_grant.creationDate = timestamp()
RETURN user, permission_grant, permission;"""
            )
            result = tx.run(query , userId = userId, role = role)
            try:
                return result[0]
            except ServiceUnavailable as exception:
                raise exception
        with self.base_resources.driver.session() as session:
            return session.write_transaction(_query)