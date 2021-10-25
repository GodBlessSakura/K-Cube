from flask import Flask, render_template, jsonify, session, g

from flask_mail import Mail
from app.config import config
from app.blueprints.admin import admin
from app.blueprints.collaborate import collaborate
from app.blueprints.comprehensive import comprehensive
from app.blueprints.draft import draft
from app.blueprints.job import job
from app.blueprints.RESTful import RESTful
from app.blueprints.uploads import uploads
from app.blueprints.user import user
import click

mail = Mail()
import os


class IncompleteRequest(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


def create_app(config_object):
    app = Flask(__name__)
    if config_object is None:
        config_object == config["default"]
    # https://stackoverflow.com/questions/26080872/secret-key-not-set-in-flask-session-using-the-flask-session-extension
    app.secret_key = "super secret key"
    app.config["SESSION_TYPE"] = "filesystem"
    app.config["upload_image_directory"] = os.path.join("uploads", "image")

    app.config.from_object(config_object)
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(collaborate, url_prefix="/collaborate")
    app.register_blueprint(comprehensive, url_prefix="/comprehensive")
    app.register_blueprint(draft, url_prefix="/draft")
    app.register_blueprint(job, url_prefix="/job")
    app.register_blueprint(RESTful, url_prefix="/RESTful")
    app.register_blueprint(uploads, url_prefix="/uploads")
    app.register_blueprint(user, url_prefix="/user")
    mail.init_app(app)
    from authorizer import UnauthorizedRequest
    from neoDB.resourcesGuard import InvalidRequest

    @app.errorhandler(UnauthorizedRequest)
    def handle_bad_request(e):
        return jsonify({"message": e.message}), 400

    @app.errorhandler(InvalidRequest)
    def handle_bad_request(e):
        return jsonify({"success": False, "message": e.message})

    @app.errorhandler(IncompleteRequest)
    def handle_bad_request(e):
        return jsonify({"success": False, "message": e.message})

    @app.route("/")
    def index():
        return render_template("index.html")

    from . import api_driver

    api_driver.init_app(app)

    @app.cli.command("set-admin")
    @click.argument("userid")
    def set_admin(userid):
        click.echo(userid)
        click.echo(
            api_driver.get_api_driver().user.assign_role(userId=userid, role="admin")
        )

    return app
