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
class graphResources:
    def __init__(self, driver):
        self.driver = driver
