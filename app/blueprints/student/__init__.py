from flask import Blueprint, render_template, abort

student = Blueprint("student", __name__, template_folder="templates")


@student.route("/")
def dashboard():
    return render_template("student/dashboard.html")
