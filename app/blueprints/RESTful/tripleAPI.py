from flask import jsonify, session, request, abort
from app.api_driver import get_api_driver
from app.authorizer import authorize_with
from neo4j.exceptions import ConstraintError

api = "/triple/"
from . import RESTful


@RESTful.route(api,methods=["GET"])
def tripleQuery():
    if request.args.get("aggregated"):
        return aggregatedTriple()


@RESTful.route(api + "<draftId>", methods=["PUT"])
@authorize_with(["canOwnDraft"])
def triplePut(draftId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().triple.create_triple(
                draftId=draftId,
                userId=session["user"]["userId"],
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})

@RESTful.route(api + "<draftId>", methods=["DELETE"])
@authorize_with(["canOwnDraft"])
def tripleDelete(draftId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().triple.remove_triple(
                draftId=draftId,
                userId=session["user"]["userId"],
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})




@RESTful.route(api + "unreachable/<draftId>", methods=["DELETE"])
@authorize_with(["canOwnDraft"])
def tripleUnreachableDelete(draftId):
    try:
        result = get_api_driver().triple.remove_unreachable_triple(
            draftId=draftId,
            userId=session["user"]["userId"],
        )
        return jsonify({"success": True, "triples": result})
    except Exception as e:
        raise e


def aggregatedTriple():
    try:
        result = get_api_driver().triple.aggregate_triple()
        return jsonify(
            {
                "success": True,
                "triples": result,
                "courses": get_api_driver().course.list_course(),
            }
        )
    except Exception as e:
        raise e
