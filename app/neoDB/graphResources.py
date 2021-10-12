from neo4j.exceptions import ConstraintError
from argon2 import PasswordHasher
from . import for_all_methods
from app import InvalidRequest
import re


def check_info(function):
    def wrapper(self, *args, **kwargs):
        if (
            "courseCode" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["courseCode"]) == None
        ):
            raise InvalidRequest("Invalid course display name pattern")
        if (
            "draftName" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["draftName"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        if (
            "userId" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{3,100}$", kwargs["userId"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        return function(self, **kwargs)

    return wrapper


@for_all_methods(check_info)
class graphResources:
    def __init__(self, driver):
        self.driver = driver
