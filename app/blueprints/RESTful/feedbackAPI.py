from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

feedback = Blueprint("feedback", __name__, url_prefix="feedback")


@feedback.get("/")
@authorize_RESTful_with(["canGiveFeedback"])
def query():
    if request.args.get("courseCode"):
        return jsonify(
            {
                "success": True,
                "feedbacks": get_api_driver().feedback.list_course_feedback(
                    courseCode=request.args.get("courseCode")
                ),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})


@feedback.get("<id>")
@authorize_RESTful_with(["canGiveFeedback"])
def get(id):
    if id is not None:
        post = get_api_driver().feedback.get_feedback(id=id)
        print(id)
        print(post)
        return jsonify(
            {
                "success": True,
                "post": get_api_driver().feedback.get_feedback(id=id),
                "replies": get_api_driver().feedback.get_reply(id=id),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})


@feedback.post("<courseCode>")
@authorize_RESTful_with(["canGiveFeedback"])
def post(courseCode):
    if "title" in request.json and "text" in request.json:
        return jsonify(
            {
                "success": True,
                "material": get_api_driver().feedback.create_feedback(
                    courseCode=courseCode,
                    userId=session["user"]["userId"],
                    title=request.json["title"],
                    text=request.json["text"],
                ),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})


@feedback.post("reply/<id>")
@authorize_RESTful_with(["canGiveFeedback"])
def postReply(id):
    if "text" in request.json:
        return jsonify(
            {
                "success": True,
                "reply": get_api_driver().feedback.create_reply(
                    userId=session["user"]["userId"],
                    id=id,
                    text=request.json["text"],
                ),
            }
        )
    return jsonify({"success": False, "message": "incomplete request"})
