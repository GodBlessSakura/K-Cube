from flask import jsonify, session, request, abort
from app.api_driver import get_api_driver
from app import InvalidRequest
from neo4j.exceptions import ConstraintError

api = "/entity/"
from . import RESTful


@RESTful.route(api + "list", methods=["GET"])
def listEntity():

    try:
        return jsonify(
            {
                "success": True,
                "entities": get_api_driver().entity.getEntities(),
            }
        )
    except Exception as e:
        raise e
    return InvalidRequest("unauthorized operation")
