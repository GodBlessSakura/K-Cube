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
            "instructor/versionTree.html",
            courseCode=courseCode,
            isInstructor=False,
            isDLTC=True,
        )
    abort(404)


@DLTC.route("/courseList")
def courseList():
    return render_template("DLTC/courseList.html")


@DLTC.route("/courseCreate")
def courseForm():
    return render_template(
        "DLTC/courseForm.html",
        imagesUrl=[
            url_for(
                "static",
                filename=current_app.config["upload_image_directory"].replace("\\", "/")
                + "/"
                + f,
            )
            for f in os.listdir(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                )
            )
            if os.path.isfile(
                os.path.join(
                    current_app.root_path,
                    "static",
                    current_app.config["upload_image_directory"],
                    f,
                )
            )
        ],
    )


@DLTC.route("/upload")
def uploadImage():
    return render_template("DLTC/uploadImage.html")
