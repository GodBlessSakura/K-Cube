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
        return jsonify(get_api_driver().admin.listPermission())
    except Exception as e:
        raise e


@RESTful.route(api, methods=["GET"])
def listUserPermission():
    if not session["permission"] or not session["permission"]["canAssignRole"]:
        return InvalidRequest("unauthorized operation")
    try:
        return jsonify(get_api_driver().admin.listUserPermission())
    except Exception as e:
        raise e


@RESTful.route(api + "<userId>", methods=["PUT"])
def assign_user_role(userId):
    if not session["permission"] or not session["permission"]["canAssignRole"]:
        return InvalidRequest("unauthorized operation")
    if "role" in request.json:
        try:
            return jsonify(
                get_api_driver().user.assign_role(
                    userId=userId, role=request.json["role"]
                )
            )
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete login request"})


@RESTful.route(api + "<userId>", methods=["DELETE"])
def remove_user_role(userId):
    if not session["permission"] or not session["permission"]["canAssignRole"]:
        return InvalidRequest("unauthorized operation")
    if "role" in request.json:
        try:
            return jsonify(
                get_api_driver().user.removeRole(
                    userId=userId, role=request.json["role"]
                )
            )
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete login request"})
