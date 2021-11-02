from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

relationship = Blueprint("relationship", __name__, url_prefix="relationship")


@relationship.get("/")
def query():
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


@authorize_RESTful_with(
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


@relationship.put("proposal")
@relationship.put("proposal/<name>")
@authorize_RESTful_with(["canProposeRelationship"], require_userId=True)
def createProposal(name):

    if name is not None:
        try:
            result = jsonify(
                get_api_driver().relationship.create_proposal(
                    userId=session["user"]["userId"], name=name
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@relationship.delete("proposal")
@relationship.delete("proposal/<name>")
@authorize_RESTful_with(["canProposeRelationship"], require_userId=True)
def removeProposal(name):
    if name is not None:
        try:
            result = jsonify(
                get_api_driver().relationship.remove_proposal(
                    userId=session["user"]["userId"], name=name
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@relationship.put("approval")
@relationship.put("approval/<name>")
@authorize_RESTful_with(["canApproveRelationship"], require_userId=True)
def createApproval(name):
    if name is not None:
        try:
            result = jsonify(
                get_api_driver().relationship.create_approval(
                    userId=session["user"]["userId"], name=name
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@relationship.put("approval")
@relationship.put("approval/<name>")
@authorize_RESTful_with(["canApproveRelationship"], require_userId=True)
def removeApproval(name):
    if name is not None:
        try:
            result = jsonify(
                get_api_driver().relationship.remove_approval(
                    userId=session["user"]["userId"], name=name
                )
            )
            return jsonify({"success": True, "message": "assign done"})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
