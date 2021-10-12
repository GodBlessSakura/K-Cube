from flask import jsonify, session, request
from app.api_driver import get_api_driver
from app import InvalidRequest

api = "/relationship/"
from . import RESTful


@RESTful.route(api)
def getRelationShipView():
    if "user" not in session or "userId" not in session["user"]:
        raise InvalidRequest("unauthorized operation")
    if not session["permission"] or (
        not session["permission"]["canProposeRelationship"]
        and not session["permission"]["canApproveRelationship"]
    ):
        raise InvalidRequest("unauthorized operation")
    try:
        return jsonify(
            {
            "success": True,
            "relationships": get_api_driver().relationship.listRelationship(userId=session["user"]["userId"])
            }
        )
    except Exception as e:
        raise e


@RESTful.route(api + "proposal", methods=["PUT", "DELETE"])
def relationshipProposal():
    if not session["permission"] or not session["permission"]["canProposeRelationship"]:
        return InvalidRequest("unauthorized operation")
    if request.method == "PUT":
        return createProposal()
    if request.method == "DELETE":
        return removeProposal()


@RESTful.route(api, methods=["PUT"])
def createProposal():
    if "name" in request.json and "user" in session and "userId" in session["user"]:
        try:
            result = jsonify(
                get_api_driver().relationship.createProposal(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@RESTful.route(api, methods=["PUT"])
def removeProposal():
    if "name" in request.json and "user" in session and "userId" in session["user"]:
        try:
            result = jsonify(
                get_api_driver().relationship.removeProposal(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@RESTful.route(api + "approval", methods=["PUT", "DELETE"])
def relationshipApproval():
    if not session["permission"] or not session["permission"]["canApproveRelationship"]:
        return InvalidRequest("unauthorized operation")
    if request.method == "PUT":
        return createApproval()
    if request.method == "DELETE":
        return removeApproval()


@RESTful.route(api, methods=["PUT"])
def createApproval():
    if "name" in request.json and "user" in session and "userId" in session["user"]:
        try:
            result = jsonify(
                get_api_driver().relationship.createApproval(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@RESTful.route(api, methods=["PUT"])
def removeApproval():
    if "name" in request.json and "user" in session and "userId" in session["user"]:
        try:
            result = jsonify(
                get_api_driver().relationship.removeApproval(
                    userId=session["user"]["userId"], name=request.json["name"]
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
