from neo4j.exceptions import ServiceUnavailable
from argon2 import PasswordHasher
from . import for_all_methods
from app import InvalidRequest
import re

# this would force the function to ignore all positional argument
def check_user_info(function):
    def wrapper(self, *args, **kwargs):
        if "email" in kwargs and len(kwargs["email"]) >= 320:
            raise InvalidRequest("A valid email should have less then 320 characters")
        if (
            "email" in kwargs
            and re.search("^[-\w\.]+@([\w-]+\.)+[\w-]{2,4}$", kwargs["email"]) == None
        ):
            raise InvalidRequest("E-mail must be in valid format")
        if (
            "userId" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{4,30}$", kwargs["userId"]) == None
        ):
            raise InvalidRequest("Invalid userId pattern.")
        if (
            "name" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,30}$", kwargs["name"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        return function(self, **kwargs)

    return wrapper


@for_all_methods(check_user_info)
class userResources:
    def __init__(self, base):
        self.driver = base

    def list_userId(self):
        def _query(tx):
            query = """MATCH (user:User)
RETURN user.userId;"""
            result = tx.run(query)
            try:
                return [record for record in result]
            except ServiceUnavailable as exception:
                raise exception

        with self.driver.session() as session:
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

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def create_user(self, userId, userName, email, password):
        ph = PasswordHasher()
        saltedHash = ph.hash(password)

        def _query(tx):
            query = """MATCH (permission:Permission{role: "restricted"})
CREATE (permission)<-[permission_grant:WEB_HAS_PERMISSION]-(user:User {userId: $userId, userName: $userName, email: $email})
-[password_set:AUTHENTICATED_BY]->(:Credential {saltedHash: $saltedHash})
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
                return dict([record for record in result][0].items())
            except ServiceUnavailable as exception:
                raise exception

        with self.driver.session() as session:
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

        with self.driver.session() as session:
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
                        return dict(rows[0]["user"].items())
                    else:
                        return None
            except ServiceUnavailable as exception:
                raise exception

        with self.driver.session() as session:
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
                    for key in row["permissions"]["properties"]:
                        if key not in permission:
                            permission[key] = row["permissions"]["properties"][key]
                        else:
                            if not permission[key]:
                                permission[key] = row["permissions"]["properties"][key]
                return dict(permission.items())
            except ServiceUnavailable as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)
