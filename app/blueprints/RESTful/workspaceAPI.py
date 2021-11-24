from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

workspace = Blueprint("workspace", __name__, url_prefix="workspace")


@workspace.post("/")
@workspace.post("/<deltaGraphId>")
@authorize_RESTful_with(["canWriteAssignedCourseBranch"])
def post(deltaGraphId):
    if "tag" in request.json and deltaGraphId is not None:
        if "triples" in request.json:
            import json

            triples = json.loads(request.json["triples"])
            return jsonify(
                {
                    "success": True,
                    "branch": get_api_driver().workspace.create_from_import(
                        deltaGraphId=request.json["deltaGraphId"],
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
# @authorize_RESTful_with(["canWriteAssignedCourseBranch"])
# def query():
#     return jsonify({"success": False, "message": "incomplete request"})


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
    return jsonify({"success": False, "message": "incomplete request"})
