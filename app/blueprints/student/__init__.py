from flask import Blueprint, render_template, abort
from app.authorizer import authorize_with

student = Blueprint("student", __name__, template_folder="templates")


@student.before_request
@authorize_with([], True, ["student", "admin"])
def middleware():
    pass

@student.route("/dashboard")
def dashboard():
    return render_template("student/dashboard.html")
