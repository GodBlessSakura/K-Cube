
from argon2 import PasswordHasher
from .resourcesGuard import for_all_methods, reject_invalid
import sys
from .cypher import cypher


@for_all_methods(reject_invalid)
class graphResources:
    def __init__(self, driver):
        self.driver = driver
