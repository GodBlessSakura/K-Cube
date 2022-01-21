class UnauthorizedRESTfulRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


from typing import Iterable
from flask import g
from functools import wraps


def authorize_RESTful_with(permissions=[], require_userId=False):
    def authorizer(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            permission_check(permissions, require_userId, UnauthorizedRESTfulRequest)
            return function(*args, **kwargs)

        return wrapper

    return authorizer


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
            permission_check(permissions, require_userId, UnauthorizedRequest)
            return function(*args, **kwargs)

        return wrapper

    return authorizer


def permission_check(
    permissions=[], require_userId=False, errorRespond=UnauthorizedRequest
):
    print(g.permission)
    if len(permissions) > 0 and "permission" not in g:
        raise errorRespond("unauthenticated user")
    for permission in permissions:
        if isinstance(permission, str):
            if (
                permission not in g.permission
                or not g.permission[permission]
            ):

                raise errorRespond("unauthorized operation")
        elif isinstance(permission, Iterable):
            at_least_one_fullfiled = False
            for or_permission in permission:
                if (
                    or_permission in g.permission
                    and g.permission[or_permission]
                ):
                    at_least_one_fullfiled = True
            if not at_least_one_fullfiled:
                raise errorRespond("unauthorized operation")

    if require_userId:
        if "user" not in session or "userId" not in session["user"]:
            raise errorRespond("unauthorized operation")
