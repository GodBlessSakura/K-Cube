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


@instructor.route("/branch/", defaults={"courseCode": None})
@instructor.route("/branch/<courseCode>")
def branch(courseCode):
    if courseCode is not None:
        return render_template("instructor/branch.html", courseCode=courseCode)
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
