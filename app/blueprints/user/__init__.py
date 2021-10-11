from flask import Blueprint, render_template, abort, redirect, request, jsonify, session
from app.api_driver import get_api_driver
from neo4j.exceptions import ConstraintError
user = Blueprint("user", __name__, template_folder="templates")


@user.route("/")
def back():
    return redirect("/")


@user.route("/profile")
def profile():
    return render_template("user/profile.html")


@user.route("/register", methods=["POST"])
def register():
    if (
        "userId" in request.json
        and "password" in request.json
        and "email" in request.json
        and "userName" in request.json
    ):
        userId = request.json["userId"]
        password = request.json["password"]
        email = request.json["email"]
        userName = request.json["userName"]
        try:
            user = get_api_driver().user.create_user(
                userId=userId, password=password, email=email, userName=userName
            )
        except ConstraintError:
            return jsonify({"success": False, "message": "The chosen UserId is already token. Choose another one."})
        
        if user:
            session["user"] = user
            try:
                print(user["userId"])
                session["permission"] = get_api_driver().user.get_user_permission(
                    userId=user["userId"]
                )
                print("permission get")
            finally:
                return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete register request"})


@user.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@user.route("/login", methods=["POST"])
def login():
    if "userId" in request.json and "password" in request.json:
        userId = request.json["userId"]
        password = request.json["password"]
        user = get_api_driver().user.authenticate_user(userId=userId, password=password)
        if user is not None:
            session["user"] = user
            try:
                session["permission"] = get_api_driver().user.get_user_permission(
                    userId=user["userId"]
                )
            except Exception as e:
                return jsonify({"success": False})
            finally:
                return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete login request"})


@user.route("/isUserIdAvaliable", methods=["GET"])
def isUserIdAvaliable():
    userId = request.args["userId"]
    return jsonify(
        {"avaliable": not get_api_driver().user.is_userId_used(userId=userId)}
    )
