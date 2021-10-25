from flask import jsonify, session, request
from app.api_driver import get_api_driver
from app.authorizer import authorize_with

api = "/role/"
from . import RESTful


@RESTful.route(api + "/permissions", methods=["GET"])
@authorize_with(["canAssignRole"])
def listPermission():
    try:
        return jsonify(
            {"permissions": get_api_driver().admin.listPermission(), "success": True}
        )
    except Exception as e:
        raise e


@RESTful.route(api, methods=["GET"])
@authorize_with(["canAssignRole"])
def listUserPermission():
    try:
        return jsonify(
            {
                "users": get_api_driver().admin.listUserPermission(),
                "success": True,
            }
        )
    except Exception as e:
        raise e


@RESTful.route(api, defaults={"userId": None}, methods=["PUT", "DELETE"])
@RESTful.route(api + "<userId>", methods=["PUT", "DELETE"])
@authorize_with(["canAssignRole"])
def put_delete_user_role(userId):
    if request.method == "PUT":
        return assign_user_role(userId)
    if request.method == "DELETE":
        return remove_user_role(userId)


def assign_user_role(userId):
    if "role" in request.json and userId is not None:
        try:
            result = jsonify(
                get_api_driver().user.assign_role(
                    userId=userId, role=request.json["role"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


def remove_user_role(userId):
    if "role" in request.json and userId is not None:
        try:
            result = get_api_driver().user.removeRole(
                userId=userId, role=request.json["role"]
            )
            return jsonify({"success": True, "message": "remove done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
