from flask import jsonify, session, request, abort
from app.api_driver import get_api_driver
from app import InvalidRequest
from neo4j.exceptions import ConstraintError

api = "/draft/"
from . import RESTful


@RESTful.route(api)
def draft():
    abort(404)


@RESTful.route(api + "list/<courseCode>", methods=["POST"])
def createDraft(courseCode):
    if (
        "permission" in session
        and "canOwnDraft" in session["permission"]
        and session["permission"]["canOwnDraft"]
    ):
        if "draftName" in request.json:
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
    return InvalidRequest("unauthorized operation")


@RESTful.route(api + "list/<courseCode>", methods=["GET"])
def listDraft(courseCode):
    if (
        "permission" in session
        and "canOwnDraft" in session["permission"]
        and session["permission"]["canOwnDraft"]
    ):
        try:
            return jsonify(
                {
                    "success": True,
                    "drafts": get_api_driver().draft.listDraft(
                        name=courseCode, userId=session["user"]["userId"]
                    ),
                }
            )
        except Exception as e:
            raise e
    return InvalidRequest("unauthorized operation")


@RESTful.route(api + "render/<draftId>", methods=["GET"])
def getGraph(draftId):
    if (
        "permission" in session
        and "canOwnDraft" in session["permission"]
        and session["permission"]["canOwnDraft"]
    ):
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
    return InvalidRequest("unauthorized operation")

@RESTful.route(api + "status", defaults={"draftId": None}, methods=["PUT"])
@RESTful.route(api + "status/<draftId>", methods=["PUT"])
def setDraftStatus(draftId):
    if (
        "permission" in session
        and "canOwnDraft" in session["permission"]
        and session["permission"]["canOwnDraft"]
    ):
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
    return InvalidRequest("unauthorized operation")
