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


@entity.get("/", defaults={"courseCode": None, "name": None})
@entity.get("/<courseCode>/", defaults={"name": None})
@entity.get("/<courseCode>/<path:name>")
def get(courseCode, name):
    if courseCode and name and request.args.get("ofUser"):
        try:
            result = get_api_driver().entity.get_user_course_entity(
                name=name, courseCode=courseCode, userId=session["user"]["userId"]
            )
            return jsonify(
                {
                    "success": True,
                    "entity": result["concept"],
                    "data": result["data"],
                }
            )
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
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


@entity.patch("/", defaults={"courseCode": None, "name": None})
@entity.patch("/<courseCode>/", defaults={"name": None})
@entity.patch("/<courseCode>/<path:name>")
def patch(courseCode, name):
    if courseCode and name and request.json.get("disambiguation"):
        try:
            result = get_api_driver().entity.entity_disambiguation(
                name=name, courseCode=courseCode, newName = request.json.get("disambiguation"), userId=session["user"]["userId"]
            )
            return jsonify(
                {
                    "success": True,
                    "entity": result["concept"],
                }
            )
        except Exception as e:
            return jsonify({"success": False, "message": str(e)})
    return jsonify({"success": False, "message": "incomplete request"})
