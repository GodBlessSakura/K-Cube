from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

workspace = Blueprint("workspace", __name__, url_prefix="workspace")


@workspace.post("/")
@workspace.post("/<deltaGraphId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def post(deltaGraphId):
    if "tag" in request.json and deltaGraphId is not None:
        if (
            "repository" in request.json
            and request.json["repository"]
            and "w_tag" in request.json
        ):
            newId = get_api_driver().workspace.create_repository(
                deltaGraphId=deltaGraphId,
                tag=request.json["tag"],
                userId=session["user"]["userId"],
                w_tag=request.json["w_tag"],
            )
            return jsonify({"success": True, "deltaGraphId": newId})
        if "triples" in request.json:
            import json

            triples = json.loads(request.json["triples"])
            return jsonify(
                {
                    "success": True,
                    "deltaGraphId": get_api_driver().workspace.create_from_import(
                        deltaGraphId=deltaGraphId,
                        tag=request.json["tag"],
                        userId=session["user"]["userId"],
                        triples=triples,
                    ),
                }
            )
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


# @workspace.get("/")
# @authorize_RESTful_with(["canWriteTeachingCourseBranch"])
# def query():
#     return jsonify({"success": False, "message": "incomplete request"})
@workspace.get("/")
def query():
    if request.args.get("lastModified") and request.args.get("courseCode"):
        return lastModifiedWorkspace(request.args.get("courseCode"))


@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def lastModifiedWorkspace(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "workspaces": get_api_driver().workspace.get_user_course_lastModified(
                    courseCode=courseCode, userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@workspace.get("<deltaGraphId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
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


@workspace.patch("/", defaults={"deltaGraphId": None})
@workspace.patch("/<deltaGraphId>")
def patch(deltaGraphId):
    if deltaGraphId is not None:
        if "sync" in request.json and request.json["sync"]:
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().workspace.sync_workspace(
                        deltaGraphId=deltaGraphId,
                        userId=session["user"]["userId"],
                    ),
                }
            )
        if (
            "checkout" in request.json
            and request.json["checkout"]
            and "deltaGraphId" in request.json
        ):
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().workspace.checkout_workspace(
                        deltaGraphId=deltaGraphId,
                        checkout=request.json["deltaGraphId"],
                        userId=session["user"]["userId"],
                    ),
                }
            )
        if "tag" in request.json:
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().workspace.rename_workspace(
                        deltaGraphId=deltaGraphId,
                        tag=request.json["tag"],
                        userId=session["user"]["userId"],
                    ),
                }
            )
    return jsonify({"success": False, "message": "incomplete request"})


@workspace.delete("/", defaults={"deltaGraphId": None})
@workspace.delete("/<deltaGraphId>")
def delete(deltaGraphId):
    if deltaGraphId is not None:
        get_api_driver().workspace.delete_workspace(
            deltaGraphId=deltaGraphId,
            userId=session["user"]["userId"],
        )
        return jsonify(
            {
                "success": True,
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})
