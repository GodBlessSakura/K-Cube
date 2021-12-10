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
from .blueprints.uploads import uploads

DLTC = Blueprint("DLTC", __name__, template_folder="templates")
DLTC.register_blueprint(uploads, url_prefix="/uploads")


@DLTC.before_request
@authorize_with(["canAccessDLTCPanel"])
def middleware():
    pass


@DLTC.route("/versionTree")
@DLTC.route("/versionTree/<courseCode>")
def versionTree(courseCode):
    if courseCode is not None:
        return render_template(
            "collegue/versionTree.html",
            courseCode=courseCode,
            isInstructor=False,
            isDLTC=True,
        )
    abort(404)


@DLTC.route("/courseList")
def courseList():
    return render_template(
        "courseList.html",
        isInstructor=False,
        isDLTC=True,
    )


@DLTC.route("/trunk/", defaults={"overwriterId": None, "overwriteeId": None})
@DLTC.route("/trunk/<overwriterId>/", defaults={"overwriteeId": None})
@DLTC.route("/trunk/<overwriterId>/<overwriteeId>")
def trunk(overwriterId, overwriteeId):
    if overwriterId is not None:
        return render_template(
            "collegue/graphCompare.html",
            overwriterId=overwriterId,
            overwriteeId=overwriteeId,
            isInstructor=False,
            isDLTC=True,
        )
    abort(404)
