from flask import jsonify, session, request, abort
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with
from neo4j.exceptions import ConstraintError

triple = Blueprint("triple", __name__, url_prefix="triple")


@triple.get("/")
def query():
    if request.args.get("aggregated"):
        return aggregatedTriple()
    return jsonify({"success": False, "message": "incomplete request"})


@triple.put("<deltaGraphId>")
@authorize_RESTful_with(["canForkAssignedCourseBranch"])
def put(deltaGraphId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().triple.create_triple(
                deltaGraphId=deltaGraphId,
                userId=session["user"]["userId"],
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@triple.delete("<deltaGraphId>")
@authorize_RESTful_with(["canForkAssignedCourseBranch"])
def delete(deltaGraphId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().triple.remove_triple(
                deltaGraphId=deltaGraphId,
                userId=session["user"]["userId"],
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@triple.delete("<deltaGraphId>/unreachable")
@authorize_RESTful_with(["canForkAssignedCourseBranch"])
def deleteUnreachable(deltaGraphId):
    try:
        result = get_api_driver().triple.remove_unreachable_triple(
            deltaGraphId=deltaGraphId,
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
