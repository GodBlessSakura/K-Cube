from flask import Blueprint, render_template, abort, current_app, url_for
import os

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.route("/")
def panel():
    return render_template(
        "admin/panel.html",
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
