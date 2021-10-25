from neo4j.exceptions import ConstraintError
from argon2 import PasswordHasher
from .resourcesGuard import for_all_methods, reject_invalid


@for_all_methods(reject_invalid)
class graphResources:
    def __init__(self, driver):
        self.driver = driver
