from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    jsonify,
)
import os
from app.authorizer import authorize_with
from app.blueprints.collaborate import collaborate
from app.api_driver import get_api_driver

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
            "/".join([admin.name, "dashboardComponents", f])
            for f in os.listdir(
                os.path.join(
                    admin.root_path,
                    admin.template_folder,
                    admin.name,
                    "dashboardComponents",
                )
            )
            if os.path.isfile(
                os.path.join(
                    admin.root_path,
                    admin.template_folder,
                    admin.name,
                    "dashboardComponents",
                    f,
                )
            )
        ]
        + [
            "/".join([collaborate.name, "dashboardComponents", f])
            for f in os.listdir(
                os.path.join(
                    collaborate.root_path,
                    collaborate.template_folder,
                    collaborate.name,
                    "dashboardComponents",
                )
            )
            if os.path.isfile(
                os.path.join(
                    collaborate.root_path,
                    collaborate.template_folder,
                    collaborate.name,
                    "dashboardComponents",
                    f,
                )
            )
        ],
    )


@admin.get("db_statistic")
def getDBStatistic():
    driver = get_api_driver()
    return jsonify(
        {
            "success": True,
            "node": driver.admin.node_statistic(),
            "edge": driver.admin.edge_statistic(),
        }
    )


@admin.route("/user")
def user_n_role():
    return render_template("admin/user_n_role.html")
