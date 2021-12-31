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
class userDAO:
    def __init__(self, driver):
        self.driver = driver

    def list_userId(self):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query)
            try:
                rows = [record for record in result]
                return [row["user.userId"] for row in rows]
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def is_userId_used(self, userId) -> bool:
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
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

        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
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
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def update_user(self, userId, userName, email):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(
                query,
                userId=userId,
                userName=userName,
                email=email,
            )
            try:
                rows = [record for record in result]
                return dict(rows[0]["user"].items())
            except Exception as exception:
                raise exception

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def assign_user_role(
        self,
        userId,
        role,
    ):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId, role=role)
            return [
                {
                    "user": dict(record["user"].items()),
                    "permission_grant": dict(record["permission_grant"].items()),
                    "permission": dict(record["permission"].items()),
                }
                for record in result
            ][0]

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def remove_user_role(
        self,
        userId,
        role,
    ):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId, role=role)
            return [
                {
                    "user": dict(record["user"].items()),
                    "permission_grant": dict(record["permission_grant"].items()),
                    "permission": dict(record["permission"].items()),
                }
                for record in result
            ][0]

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def authenticate_user(self, userId, password):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
            rows = [record for record in result]
            if len(rows) > 0:
                saltedHash = rows[0]["hash"]
                ph = PasswordHasher()
                if ph.verify(saltedHash, password):
                    return dict(rows[0]["user"].items())
                else:
                    return None

        with self.driver.session() as session:
            return session.write_transaction(_query)

    def get_user_permission(self, userId):
        fname = sys._getframe().f_code.co_name

        def _query(tx):
            query = cypher[fname + ".cyp"]
            result = tx.run(query, userId=userId)
            permission = dict()
            for row in [record for record in result]:
                for key, value in row["permissions"].items():
                    if key not in permission:
                        permission[key] = value
                    else:
                        if not permission[key]:
                            permission[key] = value
            return permission

        with self.driver.session() as session:
            return session.write_transaction(_query)
