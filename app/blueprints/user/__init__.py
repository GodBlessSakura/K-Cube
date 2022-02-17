from flask import (
    Blueprint,
    render_template,
    abort,
    redirect,
    request,
    jsonify,
    session,
    g,
    url_for,
)
from app.api_driver import get_api_driver
from neo4j.exceptions import ConstraintError
from app.authorizer import authorize_RESTful_with
from app.cache_driver import cache, user_permission, user_info

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/")
def back():
    return redirect("/")


@user.route("/refreshPermission")
@authorize_RESTful_with([], require_userId=True)
def refreshPermission():
    try:
        cache.delete_memoized(user_permission, session["user"]["userId"])
    finally:
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
            return jsonify(
                {
                    "success": False,
                    "message": "The chosen UserId is already token. Choose another one.",
                }
            )

        if user:
            session["user"] = user
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
        try:
            user = get_api_driver().user.authenticate_user(
                userId=userId, password=password
            )
            if user is not None:
                from app.cache_driver import user_permission

                session["user"] = user
                permission = user_permission(session["user"]["userId"])
                if "role" in permission:
                    if "instructor" in permission["role"]:
                        return jsonify(
                            {"success": True, "url": url_for("instructor.courseList")}
                        )
                    if "DLTC" in permission["role"]:
                        return jsonify(
                            {"success": True, "url": url_for("DLTC.courseList")}
                        )
                return jsonify({"success": True})
            return jsonify({"success": False})
        except Exception as e:
            return jsonify({"success": False})
    return jsonify({"success": False, "message": "incomplete login request"})


@user.route("/isUserIdAvaliable", methods=["GET"])
def isUserIdAvaliable():
    userId = request.args["userId"]
    return jsonify(
        {"avaliable": not get_api_driver().user.is_userId_used(userId=userId)}
    )


@user.patch("/")
def patch():
    if "userName" in request.json and "email" in request.json and "user" in session:
        user = get_api_driver().user.update_user(
            userId=session["user"]["userId"],
            email=request.json["email"],
            userName=request.json["userName"],
        )

        if user is not None:
            cache.delete_memoized(user_info, session["user"]["userId"])
            try:
                verify()
            except:
                pass
            return jsonify({"success": True})
    return jsonify({"success": False, "message": "incomplete request"})


@user.post("/verify")
@authorize_RESTful_with([], require_userId=True)
def verify():
    if "user" in session:
        if not g.user.verified:
            from ...sender import send_email

            # send_email(session["user"]["email"],
            # "email verification",
            # "")
            return jsonify(
                {"success": True, "message": "A verification is sent (not implemented)"}
            )
        return jsonify({"success": True, "message": "User already verified"})
    return jsonify({"success": False, "message": "no user session was found"})
