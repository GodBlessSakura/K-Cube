from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

trunk = Blueprint("trunk", __name__, url_prefix="trunk")


@trunk.get("/<courseCode>")
@authorize_RESTful_with([], require_userId=True)
def get(courseCode):
    edge = get_api_driver().trunk.list_trunk_branch_edge(
        courseCode=courseCode, userId=session["user"]["userId"]
    )
    node = get_api_driver().trunk.list_trunk_branch_node(
        courseCode=courseCode, userId=session["user"]["userId"]
    )
    return jsonify({"success": True, "edge": edge, "node": node})
