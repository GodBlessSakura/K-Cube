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


@DLTC.route("/course")
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
