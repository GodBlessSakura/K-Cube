class UnauthorizedRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


from typing import Iterable
from flask import session
from functools import wraps

def authorize_with(permissions=[], require_userId=False):
    def authorizer(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if len(permissions) > 0 and not session["permission"]:
                return UnauthorizedRequest("unauthenticated user")
            for permission in permissions:
                if isinstance(permission, str):
                    if not session["permission"][permission]:
                        return UnauthorizedRequest("unauthorized operation")
                elif isinstance(permission, Iterable):
                    at_least_one_fullfiled = False
                    for or_permission in permission:
                        if session["permission"][or_permission]:
                            at_least_one_fullfiled = True
                    if not at_least_one_fullfiled:
                        return UnauthorizedRequest("unauthorized operation")

            if require_userId:
                if "user" not in session or "userId" not in session["user"]:
                    raise UnauthorizedRequest("unauthorized operation")
            return function(*args, **kwargs)

        return wrapper

    return authorizer
