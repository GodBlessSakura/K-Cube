from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

graph = Blueprint("graph", __name__, url_prefix="graph")


@graph.get("compare/<overwriterId>/<overwriteeId>")
@authorize_RESTful_with(["canForkAssignedCourseBranch"])
def get_compare(overwriterId, overwriteeId):
    if overwriteeId:
        return jsonify(
            {
                "success": True,
                "overwriter": get_api_driver().workspace.get_workspace(
                    deltaGraphId=overwriterId, userId=session["user"]["userId"]
                ),
                "overwriter_triples": get_api_driver().triple.get_workspace_triple(
                    deltaGraphId=overwriterId, userId=session["user"]["userId"]
                ),
                "overwritee": get_api_driver().workspace.get_workspace_subject(
                    deltaGraphId=overwriteeId, userId=session["user"]["userId"]
                ),
                "overwritee_triples": get_api_driver().triple.get_workspace_subject_triple(
                    deltaGraphId=overwriteeId, userId=session["user"]["userId"]
                ),
            }
        )
    else:
        return jsonify(
            {
                "success": True,
                "overwriter": dict(
                    {
                        get_api_driver()
                        .workspace.get_workspace(
                            deltaGraphId=overwriterId, userId=session["user"]["userId"]
                        )
                        .items()
                        | {"labels": ["Workspace"]}.items()
                    }.items()
                ),
                "overwriter_triples": get_api_driver().triple.get_workspace_triple(
                    deltaGraphId=overwriterId, userId=session["user"]["userId"]
                ),
                "overwritee": get_api_driver().workspace.get_workspace_subject(
                    deltaGraphId=overwriterId, userId=session["user"]["userId"]
                ),
                "overwritee_triples": get_api_driver().triple.get_workspace_subject_triple(
                    deltaGraphId=overwriterId, userId=session["user"]["userId"]
                ),
            }
        )
