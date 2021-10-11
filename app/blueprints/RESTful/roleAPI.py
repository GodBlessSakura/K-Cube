from flask import jsonify, session, request
from app.api_driver import get_api_driver
from app import InvalidRequest

api = "/role/"
from . import RESTful


@RESTful.route(api + "/permissions", methods=["GET"])
def listPermission():
    if not session["permission"] or not session["permission"]["canAssignRole"]:
        return InvalidRequest("unauthorized operation")
    try:
        return jsonify(
            {"permissions": get_api_driver().admin.listPermission(), "success": True}
        )
    except Exception as e:
        raise e


@RESTful.route(api, methods=["GET"])
def listUserPermission():
    if not session["permission"] or not session["permission"]["canAssignRole"]:
        return InvalidRequest("unauthorized operation")
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
def put_delete_user_role(userId):
    if request.method == "PUT":
        return assign_user_role(userId)
    if request.method == "DELETE":
        return remove_user_role(userId)


def assign_user_role(userId):
    if not session["permission"] or not session["permission"]["canAssignRole"]:
        return InvalidRequest("unauthorized operation")
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
    if not session["permission"] or not session["permission"]["canAssignRole"]:
        return InvalidRequest("unauthorized operation")
    if "role" in request.json and userId is not None:
        try:
            result = get_api_driver().user.removeRole(
                userId=userId, role=request.json["role"]
            )

            return jsonify({"success": True, "message": "remove done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
