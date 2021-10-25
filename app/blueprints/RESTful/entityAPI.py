from flask import jsonify, session, request, abort
from app.api_driver import get_api_driver
from neo4j.exceptions import ConstraintError

api = "/entity/"
from . import RESTful


@RESTful.route(api, methods=["GET"])
def entityQuery():
    if request.args.get("list"):
        return entityList()


def entityList():

    try:
        return jsonify(
            {
                "success": True,
                "entities": get_api_driver().entity.getEntities(),
            }
        )
    except Exception as e:
        raise e
