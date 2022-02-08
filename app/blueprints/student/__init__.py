from flask import Blueprint, render_template, abort
from app.authorizer import authorize_with
import os

student = Blueprint("student", __name__, template_folder="templates")


@student.before_request
@authorize_with([], True, ["student", "admin"])
def middleware():
    pass


@student.route("/dashboard")
def dashboard():
    return render_template(
        "student/dashboard.html",
        components=[
            "/".join([student.name, "component", f])
            for f in os.listdir(
                os.path.join(
                    student.root_path,
                    student.template_folder,
                    student.name,
                    "component",
                )
            )
            if os.path.isfile(
                os.path.join(
                    student.root_path,
                    student.template_folder,
                    student.name,
                    "component",
                    f,
                )
            )
        ],
    )
