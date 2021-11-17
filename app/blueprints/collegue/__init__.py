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

collegue = Blueprint("collegue", __name__, template_folder="templates")


@collegue.before_request
@authorize_with([["canAccessDLTCPanel"], ["canAccessInstructorPanel"]])
def middleware():
    pass


@collegue.route(
    "compare/",
    defaults={
        "overwriterId": None,
        "overwriteeId": None,
    },
)
@collegue.route("compare/<overwriterId>/<overwriteeId>")
def compare(overwriterId, overwriteeId):
    if overwriterId is not None and overwriteeId is not None:
        return render_template(
            "collegue/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
            readOnly=True,
        )
    abort(404)
