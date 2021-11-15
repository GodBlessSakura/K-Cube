from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

workspace = Blueprint("workspace", __name__, url_prefix="workspace")


@workspace.put("/")
@workspace.put("/<deltaGraphId>")
@authorize_RESTful_with(["canWriteAssignedCourseBranch"])
def put(deltaGraphId):
    if "tag" in request.json and deltaGraphId is not None:
        try:
            newId = get_api_driver().workspace.create_workspace(
                deltaGraphId=deltaGraphId,
                tag=request.json["tag"],
                userId=session["user"]["userId"],
            )
            return jsonify({"success": True, "deltaGraphId": newId})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@workspace.get("/")
@authorize_RESTful_with(["canWriteAssignedCourseBranch"])
def query():
    # if request.args.get("ofUser"):
    #     return draftOfUser()
    return jsonify({"success": False, "message": "incomplete request"})


@workspace.get("<deltaGraphId>")
@authorize_RESTful_with(["canWriteAssignedCourseBranch"])
def get(deltaGraphId):
    try:
        return jsonify(
            {
                "success": True,
                "workspace": get_api_driver().workspace.get_workspace(
                    deltaGraphId=deltaGraphId, userId=session["user"]["userId"]
                ),
                "triples": get_api_driver().triple.get_workspace_triple(
                    deltaGraphId=deltaGraphId, userId=session["user"]["userId"]
                ),
                "subject": get_api_driver().workspace.get_workspace_subject(
                    deltaGraphId=deltaGraphId, userId=session["user"]["userId"]
                ),
                "subject_triples": get_api_driver().triple.get_workspace_subject_triple(
                    deltaGraphId=deltaGraphId, userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        raise e
