from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_with

course = Blueprint("course", __name__, url_prefix="course")


@course.get("/")
def query():
    if request.args.get("list"):
        return courseList()


@course.post("/")
@authorize_with(["canCreateCourse"])
def post():
    if (
        "displayName" in request.json
        and "name" in request.json
        and "imageURL" in request.json
    ):
        displayName = request.json["displayName"]
        name = request.json["name"]
        imageURL = request.json["imageURL"]
        try:
            result = get_api_driver().course.create_course(
                displayName=displayName, name=name, imageURL=imageURL
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})


def courseList():
    try:
        return jsonify(
            {"success": True, "courses": get_api_driver().course.list_course()}
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
