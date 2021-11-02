from flask import (
    Blueprint,
    render_template,
    current_app,
    url_for,
    session,
    redirect,
    abort,
)
import os

instructor = Blueprint("instructor", __name__, template_folder="templates")

