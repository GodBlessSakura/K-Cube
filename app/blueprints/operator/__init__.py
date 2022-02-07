from flask import Blueprint, render_template, abort
from app.authorizer import authorize_with

operator = Blueprint("operator", __name__, template_folder="templates")

@operator.before_request
@authorize_with([], True, ["student", "admin"])
def middleware():
    pass

@operator.route("/dashboard")
def dashboard():
    return render_template("operator/dashboard.html")
