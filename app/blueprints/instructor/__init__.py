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