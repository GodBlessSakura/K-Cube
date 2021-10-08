from flask import Blueprint, render_template, abort, redirect, request, jsonify
from app.api_driver import get_api_driver

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/")
def back():
    return redirect("/")


@user.route("/profile")
def profile():
    return render_template("user/profile.html")


@user.route("/register", methods=["POST"])
def register():
    userId = request.json["userId"]
    password = request.json["password"]


@user.route("/logout")
def logout():
    return redirect("/")


@user.route("/login", methods=["POST"])
def login():
    print(request.json)
    userId = request.json["userId"]
    password = request.json["password"]
    if userId and password:
        user = get_api_driver().user.authenticate_user(userId, password)
        if user is not None:
            session["user"] = user
            return jsonify(success=False)
            try:
                session["permission"] = get_api_driver().user.get_user_permission(
                    user["userId"]
                )

            except:
                pass
            finally:
                return jsonify(success=True)
    return jsonify(success=False)
    return str(not get_api_driver().user.is_userId_used(userId))
