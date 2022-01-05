from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

activity = Blueprint("activity", __name__, url_prefix="activity")


@activity.get("/")
def query():
    if request.args.get("ofUser") and request.args.get("courseCode"):
        return activityOfUser(session["user"]["userId"], request.args.get("courseCode"))

    if request.args.get("userId") and request.args.get("courseCode"):
        return activityOfUser(
            request.args.get("userId"), request.args.get("courseCode")
        )
    return jsonify({"success": False, "message": "incomplete request"})


def activityOfUser(userId, courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "activities": get_api_driver().activity.get_user_course_activities(
                    courseCode=courseCode, userId=userId
                ),
            }
        )
    except Exception as e:
        raise e


@activity.post("<courseCode>/", defaults={"name": None})
@activity.post("<courseCode>/<name>")
@authorize_RESTful_with(
    [["canWriteTeachingCourseMaterial", "canWriteAllCourseMaterial"]]
)
def post(courseCode, name):
    if "desc" in request.json and "week" in request.json:
        return jsonify(
            {
                "success": True,
                "activity": get_api_driver().activity.set_user_course_activities(
                    courseCode=courseCode,
                    name=name,
                    week=int(request.json["week"]),
                    userId=session["user"]["userId"],
                    desc=request.json["desc"],
                ),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})