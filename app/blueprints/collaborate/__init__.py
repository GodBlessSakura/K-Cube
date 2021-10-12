from flask import Blueprint, render_template, abort, current_app, url_for

collaborate = Blueprint("collaborate", __name__, template_folder="templates")


@collaborate.route("/")
def index():
    return render_template("collaborate/index.html")
