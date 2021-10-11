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
        and "displayName" in request.json
        and "imageURL" in request.json
    ):
        displayName = request.json["displayName"]
        name = request.json["name"]
        imageURL = request.json["imageURL"]
        get_api_driver().course.courseResources(displayName, name, imageURL)
    return jsonify({"success": False, "message": "incomplete request"})
