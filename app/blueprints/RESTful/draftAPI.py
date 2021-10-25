from flask import jsonify, session, request, abort
from app.api_driver import get_api_driver
from app.authorizer import authorize_with
from neo4j.exceptions import ConstraintError

api = "/draft/"
from . import RESTful


@RESTful.route(api, methods=["GET"])
@authorize_with(["canOwnDraft"])
def draftQuery():
    if request.args.get("ofUser"):
        return draftOfUser()


@RESTful.route(api + "<courseCode>", methods=["POST"])
@authorize_with(["canOwnDraft"])
def draftPost(courseCode):
    if "draftName" in request.json:
        if request.args.get("clone"):
            return cloneDraft()
        try:
            return jsonify(
                {
                    "success": True,
                    "drafts": get_api_driver().draft.createDraft(
                        name=courseCode,
                        userId=session["user"]["userId"],
                        draftName=request.json["draftName"],
                    ),
                }
            )
        except ConstraintError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Draft with same name already exists, try another name.",
                }
            )
    return jsonify({"success": False, "message": "incomplete request"})


def cloneDraft():
    if (
        "draftName" in request.json
        and "name" in request.json
        and "sourceDraftId" in request.json
    ):
        try:
            return jsonify(
                {
                    "success": True,
                    "drafts": get_api_driver().draft.cloneDraft(
                        name=request.json["name"],
                        userId=session["user"]["userId"],
                        draftName=request.json["draftName"],
                        draftId=request.json["sourceDraftId"],
                    ),
                }
            )
        except ConstraintError as e:
            return jsonify(
                {
                    "success": False,
                    "message": "Draft with same name already exists, try another name.",
                }
            )
    return jsonify({"success": False, "message": "incomplete request"})


def draftOfUser(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "drafts": get_api_driver().draft.draftOfUser(
                    name=courseCode, userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


@RESTful.route(api + "draftTriples/<draftId>", methods=["GET"])
@authorize_with(["canOwnDraft"])
def draftTriples(draftId):
    try:
        return jsonify(
            {
                "success": True,
                "draft": get_api_driver().draft.getDraft(
                    draftId=draftId, userId=session["user"]["userId"]
                ),
                "triples": get_api_driver().triple.getTriples(
                    draftId=draftId, userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


@RESTful.route(api + "status/<draftId>", methods=["PUT"])
@authorize_with(["canOwnDraft"])
def draftStatusPut(draftId):
    if "status" in request.json:
        try:
            return jsonify(
                {
                    "success": True,
                    "status": get_api_driver().draft.setStatus(
                        draftId=draftId,
                        userId=session["user"]["userId"],
                        status=request.json["status"],
                    ),
                }
            )
        except Exception as e:
            raise e
