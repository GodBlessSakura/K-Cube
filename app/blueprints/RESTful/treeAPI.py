from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

tree = Blueprint("tree", __name__, url_prefix="tree")


@tree.get("/<courseCode>")
@authorize_RESTful_with([], require_userId=True)
def get(courseCode):
    branch_edges = get_api_driver().branch.list_course_branch_edge(
        courseCode=courseCode, userId=session["user"]["userId"]
    )
    branch_nodes = get_api_driver().branch.list_course_branch_node(
        courseCode=courseCode, userId=session["user"]["userId"]
    )
    trunk_edges = get_api_driver().trunk.list_course_trunk_edge(courseCode=courseCode)
    trunk_nodes = get_api_driver().trunk.list_course_trunk_node(courseCode=courseCode)

    return jsonify(
        {
            "success": True,
            "edges": branch_edges + trunk_edges,
            "branch_nodes": branch_nodes,
            "trunk_nodes": trunk_nodes
        }
    )
