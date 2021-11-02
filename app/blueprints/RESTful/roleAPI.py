from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_with

role = Blueprint("role", __name__, url_prefix="role")


@role.get("/")
@authorize_with(["canAssignRole"])
def query():
    if request.args.get("listRolePermission"):
        return roleList()
    if request.args.get("listUser"):
        return listUserRole()


def roleList():
    try:
        return jsonify(
            {"permissions": get_api_driver().admin.list_role(), "success": True}
        )
    except Exception as e:
        raise e


def listUserRole():
    try:
        return jsonify(
            {
                "users": get_api_driver().admin.list_user_role(),
                "success": True,
            }
        )
    except Exception as e:
        raise e

@role.put("/")
@role.put("<userId>")
@authorize_with(["canAssignRole"])
def put(userId):
    if "role" in request.json and userId is not None:
        try:
            result = jsonify(
                get_api_driver().user.assign_user_role(
                    userId=userId, role=request.json["role"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})

@role.delete("/")
@role.delete("<userId>")
@authorize_with(["canAssignRole"])
def delete(userId):
    if "role" in request.json and userId is not None:
        try:
            result = get_api_driver().user.remove_user_role(
                userId=userId, role=request.json["role"]
            )
            return jsonify({"success": True, "message": "remove done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
