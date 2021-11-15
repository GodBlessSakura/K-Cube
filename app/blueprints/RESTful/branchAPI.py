from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

branch = Blueprint("branch", __name__, url_prefix="branch")


@branch.post("/<overwriterId>/", defaults={"overwriteeId": None})
@branch.post("/<overwriterId>/<overwriteeId>")
def post(overwriterId, overwriteeId):
    if "tag" in request.json and "action" in request.json:
        if overwriterId is not None and overwriteeId is None:
            if request.json["action"] == "fork":
                return jsonify(
                    {
                        "success": True,
                        "branch": get_api_driver().workspace.commit_workspace_as_fork(
                            deltaGraphId=overwriterId,
                            tag=request.json["tag"],
                            userId=session["user"]["userId"],
                        ),
                    }
                )
            if request.json["action"] == "patch":
                return jsonify(
                    {
                        "success": True,
                        "branch": get_api_driver().workspace.commit_workspace_as_patch(
                            overwriterId=overwriterId,
                            overwriteeId=overwriteeId,
                            tag=request.json["tag"],
                            userId=session["user"]["userId"],
                        ),
                    }
                )
        if overwriterId is not None and overwriteeId is not None:
            if request.json["action"] == "fork":
                return jsonify(
                    {
                        "success": True,
                        "branch": get_api_driver().branch.merge_as_fork(
                            overwriterId=overwriterId,
                            overwriteeId=overwriteeId,
                            tag=request.json["tag"],
                            userId=session["user"]["userId"],
                        ),
                    }
                )
            if request.json["action"] == "patch":
                return jsonify(
                    {
                        "success": True,
                        "branch": get_api_driver().branch.merge_as_patch(
                            overwriterId=overwriterId,
                            overwriteeId=overwriteeId,
                            tag=request.json["tag"],
                            userId=session["user"]["userId"],
                        ),
                    }
                )
    return jsonify({"success": False, "message": "incomplete request"})


@branch.patch("/", defaults={"deltaGraphId": None})
@branch.patch("/<deltaGraphId>")
def patch(deltaGraphId):
    if deltaGraphId is not None:
        if "canPush" in request.json:
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().branch.set_canPush(
                        deltaGraphId=deltaGraphId,
                        userId=session["user"]["userId"],
                        canPush=request.json["canPush"],
                    ),
                }
            )
    return jsonify({"success": False, "message": "incomplete request"})
