from flask import Blueprint, render_template, session, redirect, abort

collaborate = Blueprint("collaborate", __name__, template_folder="templates")


@collaborate.route("/")
def index():
    if (
        "permission" in session
        and "canProposeRelationship" in session["permission"]
        and session["permission"]["canProposeRelationship"]
    ):
        return render_template("collaborate/index.html")
    abort(404)
