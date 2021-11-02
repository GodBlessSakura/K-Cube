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

DLTC = Blueprint("DLTC", __name__, template_folder="templates")


@DLTC.route("/course")
def courseForm():
    if (
        "permission" in session
        and "canAccessAdminPanel" in session["permission"]
        and session["permission"]["canAccessAdminPanel"]
    ):
        return render_template(
            "DLTC/courseForm.html",
            imagesUrl=[
                url_for(
                    "static",
                    filename=current_app.config["upload_image_directory"].replace(
                        "\\", "/"
                    )
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
    abort(404)


@DLTC.route("/upload")
def uploadImage():
    if (
        "permission" in session
        and "canAccessAdminPanel" in session["permission"]
        and session["permission"]["canAccessAdminPanel"]
    ):
        return render_template("DLTC/uploadImage.html")
    abort(404)
