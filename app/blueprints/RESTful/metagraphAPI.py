from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

metagraph = Blueprint("metagraph", __name__, url_prefix="metagraph")


@metagraph.get("/")
def query():
    if request.args.get("concepts"):
        return jsonify(
            {
                "success": True,
                "concepts": get_api_driver().metagraph.list_metagraph_concept(),
            }
        )
    if request.args.get("triples"):
        return jsonify(
            {
                "success": True,
                "triples": get_api_driver().metagraph.list_metagraph_triple(),
            }
        )


@metagraph.put("/")
@authorize_RESTful_with(["canCreateCourse"])
def put():
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().metagraph.create_metagraph_triple(
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})


@metagraph.delete("/")
@authorize_RESTful_with(["canCreateCourse"])
def delete():
    if (
        "h_name" in request.json
        and "r_name" in request.json
        and "t_name" in request.json
    ):
        try:
            result = get_api_driver().metagraph.delete_metagraph_triple(
                h_name=request.json["h_name"],
                r_name=request.json["r_name"],
                t_name=request.json["t_name"],
            )
            return jsonify({"success": True, "triple": result})
        except Exception as e:
            raise e
    return jsonify({"success": False, "message": "incomplete request"})
