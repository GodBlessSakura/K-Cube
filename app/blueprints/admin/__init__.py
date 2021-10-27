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

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/panel")
def panel():
    if (
        "permission" in session
        and "canAccessAdminPanel" in session["permission"]
        and session["permission"]["canAccessAdminPanel"]
    ):
        return render_template("admin/panel.html")
    abort(404)


@admin.route("/course")
def courseForm():
    if (
        "permission" in session
        and "canAccessAdminPanel" in session["permission"]
        and session["permission"]["canAccessAdminPanel"]
    ):
        return render_template(
            "admin/courseForm.html",
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


@admin.route("/upload")
def uploadImage():
    if (
        "permission" in session
        and "canAccessAdminPanel" in session["permission"]
        and session["permission"]["canAccessAdminPanel"]
    ):
        return render_template("admin/uploadImage.html")
    abort(404)


@admin.route("/user")
def user_n_role():
    if (
        "permission" in session
        and "canAccessAdminPanel" in session["permission"]
        and session["permission"]["canAccessAdminPanel"]
    ):
        return render_template("admin/user_n_role.html")
    abort(404)
