from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    abort,
)
import os
from app.authorizer import authorize_with

instructor = Blueprint("instructor", __name__, template_folder="templates")


@instructor.before_request
@authorize_with(["canAccessInstructorPanel"])
def middleware():
    pass


@instructor.route("/courseList")
def courseList():
    return render_template("instructor/courseList.html")


@instructor.route("/versionTree/", defaults={"courseCode": None})
@instructor.route("/versionTree/<courseCode>")
def versionTree(courseCode):
    if courseCode is not None:
        return render_template(
            "instructor/versionTree.html",
            courseCode=courseCode,
            isInstructor=True,
            isDLTC=False,
        )
    abort(404)


@instructor.route("/courseSchedule/", defaults={"courseCode": None})
@instructor.route("/courseSchedule/<courseCode>")
def courseSchedule(courseCode):
    if courseCode is not None:
        return render_template("instructor/courseList.html", courseCode=courseCode)
    abort(404)


@instructor.route("/resources/", defaults={"courseCode": None})
@instructor.route("/resources/<courseCode>")
def resources(courseCode):
    if courseCode is not None:
        return render_template("instructor/courseList.html", courseCode=courseCode)
    abort(404)


@instructor.route("/schedule")
def schedule():
    return render_template("instructor/courseList.html")


@instructor.route("/workspace/", defaults={"deltaGraphId": None})
@instructor.route("/workspace/<deltaGraphId>")
def workspace(deltaGraphId):
    if deltaGraphId is not None:
        return render_template("instructor/graphEditor.html", deltaGraphId=deltaGraphId)
    abort(404)


@instructor.route(
    "/workspace/commit/", defaults={"overwriterId": None, "overwriteeId": None}
)
@instructor.route("/workspace/commit/<overwriterId>/", defaults={"overwriteeId": None})
@instructor.route("/workspace/commit/<overwriterId>/<overwriteeId>")
def commit(overwriterId, overwriteeId):
    if overwriterId is not None:
        return render_template(
            "instructor/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
            isInstructor=True,
            isDLTC=False,
        )
    abort(404)

@instructor.route(
    "/branch/", defaults={"overwriterId": None, "overwriteeId": None}
)
@instructor.route("/branch/<overwriterId>/", defaults={"overwriteeId": None})
@instructor.route("/branch/<overwriterId>/<overwriteeId>")
def branch(overwriterId, overwriteeId):
    if overwriterId is not None:
        return render_template(
            "instructor/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
            isInstructor=True,
            isDLTC=False,
        )
    abort(404)