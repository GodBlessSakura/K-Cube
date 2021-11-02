from flask import jsonify, session, request, abort
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_with
from neo4j.exceptions import ConstraintError

draft = Blueprint("draft", __name__, url_prefix="draft")


@draft.get("/")
@authorize_with(["canOwnDraft"])
def query():
    if request.args.get("ofUser"):
        return draftOfUser()


@draft.post("<courseCode>")
@authorize_with(["canOwnDraft"])
def post(courseCode):
    if "draftName" in request.json:
        if request.args.get("clone"):
            return cloneDraft()
        try:
            return jsonify(
                {
                    "success": True,
                    "drafts": get_api_driver().draft.create_draft(
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
                    "drafts": get_api_driver().draft.clone_draft(
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
                "drafts": get_api_driver().draft.list_a_user_draft(
                    name=courseCode, userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


@draft.get("<draftId>")
@authorize_with(["canOwnDraft"])
def get(draftId):
    try:
        return jsonify(
            {
                "success": True,
                "draft": get_api_driver().draft.get_draft(
                    draftId=draftId, userId=session["user"]["userId"]
                ),
                "triples": get_api_driver().triple.get_draft_triple(
                    draftId=draftId, userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


@draft.put("<draftId>")
@authorize_with(["canOwnDraft"])
def put(draftId):
    if "status" in request.json:
        try:
            return jsonify(
                {
                    "success": True,
                    "status": get_api_driver().draft.set_draft_status(
                        draftId=draftId,
                        userId=session["user"]["userId"],
                        status=request.json["status"],
                    ),
                }
            )
        except Exception as e:
            raise e
