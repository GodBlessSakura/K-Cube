from flask import jsonify, session, request
from app.api_driver import get_api_driver
from app import InvalidRequest

api = "/course/"
from . import RESTful


@RESTful.route(api, methods=["POST"])
def courseCreate():
    if not session["permission"] or not session["permission"]["canCreateCourse"]:
        return InvalidRequest("unauthorized operation")
    if (
        "displayName" in request.json
        and "name" in request.json
        and "imageURL" in request.json
    ):
        displayName = request.json["displayName"]
        name = request.json["name"]
        imageURL = request.json["imageURL"]
        try:
            result = get_api_driver().course.courseCreate(
                displayName=displayName, name=name, imageURL=imageURL
            )
            return jsonify({"success": True})
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})


@RESTful.route(api, methods=["GET"])
def listCourse():
    try:
        return jsonify(
            {"success": True, "courses": get_api_driver().course.listCourse()}
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
