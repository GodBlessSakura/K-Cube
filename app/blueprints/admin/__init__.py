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


@admin.route("/")
def panel():
    if (
        "permission" in session
        and "canAccessAdminPanel" in session["permission"]
        and session["permission"]["canAccessAdminPanel"]
    ):
        return render_template(
            "admin/index.html",
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
