from flask import Blueprint, render_template, abort, redirect, request, jsonify, session
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
    email = request.json["email"]
    userName = request.json["userName"]
    if userId and password and email and userName:
        user = get_api_driver().user.create_user(
            userId=userId, password=password, email=email, userName=userName
        )
        if user:
            session["user"] = user
            try:
                session["permission"] = get_api_driver().user.get_user_permission(
                    userId=user["userId"]
                )

            except:
                pass
            finally:
                return jsonify({"success":True})
    return jsonify({"success":False})


@user.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@user.route("/login", methods=["POST"])
def login():
    userId = request.json["userId"]
    password = request.json["password"]
    if userId and password:
        user = get_api_driver().user.authenticate_user(userId=userId, password=password)
        if user is not None:
            session["user"] = user
            try:
                session["permission"] = get_api_driver().user.get_user_permission(
                    userId=user["userId"]
                )
                print(session["permission"])

            except Exception as e:
                print(e)
            finally:
                return jsonify({"success":True})
    return jsonify({"success":False})
