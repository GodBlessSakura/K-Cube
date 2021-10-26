from flask import jsonify, session, request
from app.api_driver import get_api_driver
from app.authorizer import authorize_with

api = "/relationship/"
from . import RESTful


@RESTful.route(api, methods=["GET"])
def relationshipQuery():
    if request.args.get("approved"):
        return listApprovedRelationships()
    if request.args.get("userView"):
        return getRelationShipView()


def listApprovedRelationships():
    try:
        return jsonify(
            {
                "success": True,
                "relationships": get_api_driver().relationship.list_approved_relationship(),
            }
        )
    except Exception as e:
        raise e


@authorize_with(
    [["canProposeRelationship", "canApproveRelationship"]], require_userId=True
)
def getRelationShipView():
    try:
        return jsonify(
            {
                "success": True,
                "relationships": get_api_driver().relationship.list_relationship(
                    userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        raise e


@RESTful.route(api + "proposal", methods=["PUT", "DELETE"])
@authorize_with(["canProposeRelationship"], require_userId=True)
def relationshipProposal():
    if request.method == "PUT":
        return createProposal()
    if request.method == "DELETE":
        return removeProposal()


@RESTful.route(api + "proposal", methods=["PUT"])
def createProposal():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.create_proposal(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@RESTful.route(api + "proposal", methods=["DELETE"])
def removeProposal():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.remove_proposal(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@RESTful.route(api + "approval", methods=["PUT", "DELETE"])
@authorize_with(["canApproveRelationship"], require_userId=True)
def relationshipApproval():
    if request.method == "PUT":
        return createApproval()
    if request.method == "DELETE":
        return removeApproval()


@RESTful.route(api + "approval", methods=["PUT"])
def createApproval():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.create_approval(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@RESTful.route(api + "approval", methods=["PUT"])
def removeApproval():
    if "name" in request.json:
        try:
            result = jsonify(
                get_api_driver().relationship.remove_approval(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
