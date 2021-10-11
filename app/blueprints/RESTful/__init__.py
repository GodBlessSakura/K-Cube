from flask import Blueprint, render_template, abort

RESTful = Blueprint("RESTful", __name__)
from . import courseAPI
from . import draftAPI
from . import graphAPI