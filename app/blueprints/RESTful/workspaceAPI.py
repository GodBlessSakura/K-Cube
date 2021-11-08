from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

workspace = Blueprint("workspace", __name__, url_prefix="workspace")


@workspace.put("/")
@workspace.put("/<deltaGraphId>")
@authorize_RESTful_with(["canForkAssignedCourseBranch"])
def put(deltaGraphId):
    if "tag" in request.json and deltaGraphId is not None:
        try:
            id = get_api_driver().workspace.create_workspace(
                deltaGraphId=deltaGraphId,
                tag=request.json["tag"],
                userId=session["user"]["userId"],
            )
            return jsonify({"success": True, "deltaGraphId": id})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
