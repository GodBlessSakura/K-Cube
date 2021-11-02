from flask import jsonify, session, request
from flask.blueprints import Blueprint
from app.api_driver import get_api_driver
from app.authorizer import authorize_RESTful_with

workspace = Blueprint("workspace", __name__, url_prefix="workspace")