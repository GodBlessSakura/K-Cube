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
@authorize_with(["canAccessAdminPanel"])
def middleware():
    pass


@admin.route("/panel")
def panel():
    return render_template("admin/panel.html")


@admin.route("/user")
def user_n_role():
    return render_template("admin/user_n_role.html")
