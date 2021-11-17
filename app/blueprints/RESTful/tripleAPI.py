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


@triple.get("/course/", defaults={"courseCode": None})
@triple.get("/course/<courseCode>")
def getCourse(courseCode):
    if courseCode is not None:
        result = get_api_driver().triple.get_course_triple(courseCode=courseCode)
        return jsonify(
            {
                "success": True,
                "triples": result,
                "course": get_api_driver().course.get_course(courseCode=courseCode),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})


@triple.put("<deltaGraphId>")
@authorize_RESTful_with(["canWriteAssignedCourseBranch"])
def put(deltaGraphId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
        and "r_value" in request.json
    ):
        try:
            result = get_api_driver().triple.set_workspace_triple(
                deltaGraphId=deltaGraphId,
                userId=session["user"]["userId"],
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
                r_value=request.json["r_value"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@triple.delete("<deltaGraphId>")
@authorize_RESTful_with(["canWriteAssignedCourseBranch"])
def delete(deltaGraphId):
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().triple.remove_workspace_triple(
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
@authorize_RESTful_with(["canWriteAssignedCourseBranch"])
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
        result = get_api_driver().triple.get_aggregated_triple()
        return jsonify(
            {
                "success": True,
                "triples": result,
                "courses": get_api_driver().course.list_course(),
            }
        )
    except Exception as e:
        raise e
