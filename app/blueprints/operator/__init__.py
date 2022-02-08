from flask import Blueprint, render_template, abort
from app.authorizer import authorize_with
import os

operator = Blueprint("operator", __name__, template_folder="templates")

@operator.before_request
@authorize_with([], True, ["student", "admin"])
def middleware():
    pass

@operator.route("/dashboard")
def dashboard():
    return render_template("operator/dashboard.html",
        components=[
            "/".join([operator.name, "component", f])
            for f in os.listdir(
                os.path.join(
                    operator.root_path,
                    operator.template_folder,
                    operator.name,
                    "component",
                )
            )
            if os.path.isfile(
                os.path.join(
                    operator.root_path,
                    operator.template_folder,
                    operator.name,
                    "component",
                    f,
                )
            )
        ],)
