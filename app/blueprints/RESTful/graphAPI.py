from flask import jsonify, session, request, g
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

graph = Blueprint("graph", __name__, url_prefix="graph")


@graph.get("/compare/<overwriterId>/", defaults={"overwriteeId": None})
@graph.get("compare/<overwriterId>/<overwriteeId>")
@authorize_RESTful_with(["canWriteTeachingCourseBranch"])
def get_compare(overwriterId, overwriteeId):
    if overwriteeId:
        return jsonify(
            {
                "success": True,
                "overwriter": get_api_driver().graph.get_graph(
                    deltaGraphId=overwriterId, userId=g.user["userId"]
                ),
                "overwriter_triples": get_api_driver().triple.get_graph_triple(
                    deltaGraphId=overwriterId, userId=g.user["userId"]
                ),
                "overwritee": get_api_driver().graph.get_graph(
                    deltaGraphId=overwriteeId, userId=g.user["userId"]
                ),
                "overwritee_triples": get_api_driver().triple.get_graph_triple(
                    deltaGraphId=overwriteeId, userId=g.user["userId"]
                ),
            }
        )
    else:
        return jsonify(
            {
                "success": True,
                "overwriter": dict(
                    get_api_driver()
                    .workspace.get_workspace(
                        deltaGraphId=overwriterId, userId=g.user["userId"]
                    )
                    .items(),
                    labels=["Workspace"],
                ),
                "overwriter_triples": get_api_driver().triple.get_workspace_triple(
                    deltaGraphId=overwriterId, userId=g.user["userId"]
                ),
                "overwritee": get_api_driver().workspace.get_workspace_subject(
                    deltaGraphId=overwriterId, userId=g.user["userId"]
                ),
                "overwritee_triples": get_api_driver().triple.get_workspace_subject_triple(
                    deltaGraphId=overwriterId, userId=g.user["userId"]
                ),
            }
        )


@graph.get("/<deltaGraphId>/")
def get(deltaGraphId):
    return jsonify(
        {
            "success": True,
            "graph": get_api_driver().graph.get_graph(
                deltaGraphId=deltaGraphId, userId=g.user["userId"]
            ),
            "triples": get_api_driver().triple.get_graph_triple(
                deltaGraphId=deltaGraphId, userId=g.user["userId"]
            ),
        }
    )
