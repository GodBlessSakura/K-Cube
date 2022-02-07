from flask import Blueprint, render_template, abort

operator = Blueprint("operator", __name__, template_folder="templates")


@operator.route("/")
def dashboard():
    return render_template("operator/dashboard.html")
