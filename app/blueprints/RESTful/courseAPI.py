from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

course = Blueprint("course", __name__, url_prefix="course")


@course.get("/")
def query():
    if request.args.get("list"):
        return courseList()
    if request.args.get("instructor") and request.args.get("courseCode") is not None:
        return courseInstructor(request.args.get("courseCode"))
    if request.args.get("user"):
        return userCourse()
    if request.args.get("graphs") and request.args.get("courseCode") is not None:
        return courseInstructorGraph(request.args.get("courseCode"))
    return jsonify({"success": False, "message": "incomplete request"})



@authorize_RESTful_with([], require_userId=True)
def userCourse():
    try:
        return jsonify(
            {
                "success": True,
                "courses": get_api_driver().course.list_instructor_course(
                    userId=session["user"]["userId"]
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@course.post("/")
@authorize_RESTful_with(["canCreateCourse"])
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


def courseInstructor(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "instructors": get_api_driver().course.list_course_instructor(
                    courseCode=courseCode
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

def courseInstructorGraph(courseCode):
    try:
        return jsonify(
            {
                "success": True,
                "instructors": get_api_driver().course.list_course_graph(
                    courseCode=courseCode
                ),
            }
        )
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

@course.patch("/", defaults={"courseCode": None})
@course.patch("<courseCode>")
@authorize_RESTful_with(["canAssignCourse"])
def patch(courseCode):
    if courseCode is not None:
        if "assignment" in request.json and "userId" in request.json:
            if request.json["assignment"]:
                get_api_driver().course.assign_course_instructor(
                    courseCode=courseCode, userId=request.json["userId"]
                )
                return jsonify({"success": True})
            else:
                get_api_driver().course.unassign_course_instructor(
                    courseCode=courseCode, userId=request.json["userId"]
                )
                return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete request"})
