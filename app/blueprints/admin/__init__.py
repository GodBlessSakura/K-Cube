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

admin = Blueprint("admin", __name__, template_folder="templates")


@admin.before_request
@authorize_with([], True, ["admin"])
def middleware():
    pass


@admin.route("/dashboard")
def dashboard():
    print()
    return render_template(
        "admin/dashboard.html",
        components=[
            "/".join([admin.name, "component", f])
            for f in os.listdir(
                os.path.join(
                    admin.root_path,
                    admin.template_folder,
                    admin.name,
                    "component",
                )
            )
            if os.path.isfile(
                os.path.join(
                    admin.root_path,
                    admin.template_folder,
                    admin.name,
                    "component",
                    f,
                )
            )
        ],
    )


@admin.route("/user")
def user_n_role():
    return render_template("admin/user_n_role.html")
