# https://stackoverflow.com/questions/6307761/how-to-decorate-all-functions-of-a-class-without-typing-it-over-and-over-for-eac
# example:
# @for_all_methods(sanitize_args_and_kwargs)
# class userResources:
def for_all_methods(decorator):
    def wrapper(cls):
        for attr in cls.__dict__:  # there's propably a better way to do this
            if callable(getattr(cls, attr)):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls

    return wrapper


# the actual sanitize logic's implementation
def sanitize(value):

    return value


def sanitize_args_and_kwargs(function):
    def wrapper(*args, **kwargs):
        for each in args:
            each = sanitize(each)
        for key in kwargs:
            kwargs[key] = sanitize(kwargs[key])
        return function(*args, **kwargs)

    return wrapper


class InvalidRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


import re

# this would force the function to ignore all positional argument
def reject_invalid(function):
    def wrapper(self, *args, **kwargs):
        if (
            "courseCode" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["courseCode"]) == None
        ):
            raise InvalidRequest("Invalid course code pattern")
        if (
            "draftName" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["draftName"]) == None
        ):
            raise InvalidRequest("Invalid draft name pattern.")
        if (
            "userId" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{3,100}$", kwargs["userId"]) == None
        ):
            raise InvalidRequest("Invalid userId pattern.")
        if (
            "ownerId" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{3,100}$", kwargs["ownerId"]) == None
        ):
            raise InvalidRequest("Invalid ownerId pattern.")
        if "visibility" in kwargs and kwargs["visibility"] not in ["private", "collaborator", "instructor", "colleague", "public"]:
            raise InvalidRequest("Invalid status pattern.")
        if "email" in kwargs and len(kwargs["email"]) >= 320:
            raise InvalidRequest("A valid email should have less then 320 characters")
        if (
            "email" in kwargs
            and re.search("^[-\w\.]+@([\w-]+\.)+[\w-]{2,4}$", kwargs["email"]) == None
        ):
            raise InvalidRequest("E-mail must be in valid format")
        if (
            "name" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["name"]) == None
        ):
            raise InvalidRequest("Invalid name pattern.")
        if (
            "h_name" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["h_name"]) == None
        ):
            raise InvalidRequest("Invalid head entity name pattern.")
        if (
            "r_name" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["r_name"]) == None
        ):
            raise InvalidRequest("Invalid relationship name pattern.")
        if (
            "t_name" in kwargs
            and re.search("^[a-zA-Z0-9\s]{4,100}$", kwargs["t_name"]) == None
        ):
            raise InvalidRequest("Invalid tail entity name pattern.")
        if (
            "h_name" in kwargs
            and "t_name" in kwargs
            and kwargs["h_name"] == kwargs["t_name"]
        ):
            raise InvalidRequest(
                "Invalid triple pattern, self-referencing is not allowed."
            )
        if "text" in kwargs and (len(kwargs["text"]) < 4 or len(kwargs["text"]) > 500):
            raise InvalidRequest("Invalid text pattern.")
        if (
            "desc" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{3,500}$", kwargs["desc"]) == None
        ):
            raise InvalidRequest("Invalid text pattern.")
        if (
            "title" in kwargs
            and re.search("^[a-zA-Z][a-zA-Z0-9]{3,500}$", kwargs["title"]) == None
        ):
            raise InvalidRequest("Invalid text pattern.")
        if "week" in kwargs and (kwargs["text"] < 1 or kwargs["text"] > 13):
            raise InvalidRequest("Invalid week value.")
        if (
            "tag" in kwargs
            and re.search("^[a-zA-Z0-9\s.]{4,100}$", kwargs["tag"]) == None
        ):
            raise InvalidRequest("Invalid tag pattern.")
        if "r_value" in kwargs and not isinstance(kwargs["r_value"], bool):
            raise InvalidRequest("Invalid r_value.")
        return function(self, **kwargs)

    return wrapper
