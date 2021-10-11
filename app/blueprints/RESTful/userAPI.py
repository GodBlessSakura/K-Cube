from flask import request, session, jsonify
from app.api_driver import get_api_driver
from . import RESTful


@RESTful.route("/user/isUserIdAvaliable", methods=["GET"])
def isUserIdAvaliable():
    userId = request.args["userId"]
    return jsonify(
        {"avaliable": not get_api_driver().user.is_userId_used(userId=userId)}
    )
