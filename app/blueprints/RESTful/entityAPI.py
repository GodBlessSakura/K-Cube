from flask import jsonify, session, request, abort
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from neo4j.exceptions import ConstraintError

entity = Blueprint("entity", __name__, url_prefix="entity")


@entity.get("/")
def query():
    if request.args.get("list"):
        return entityList()
    return jsonify({"success": False, "message": "incomplete request"})


def entityList():

    try:
        return jsonify(
            {
                "success": True,
                "entities": get_api_driver().entity.list_entity(),
            }
        )
    except Exception as e:
        raise e
