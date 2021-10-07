from flask import Flask, render_template
from flask_mail import Mail
from app.config import config
from app.blueprints.admin import admin
from app.blueprints.comprehensive import comprehensive
from app.blueprints.draft import draft
from app.blueprints.job import job
from app.blueprints.RESTful import RESTful
from app.blueprints.uploads import uploads
from app.blueprints.user import user
import click

from flask.cli import FlaskGroup
mail = Mail()


def create_app(config_object):
    app = Flask(__name__)
    if config_object is None:
        config_object == config['default']
    app.config.from_object(config_object)
    app.register_blueprint(admin, url_prefix="/admin")
    app.register_blueprint(comprehensive, url_prefix="/comprehensive")
    app.register_blueprint(draft, url_prefix="/draft")
    app.register_blueprint(job, url_prefix="/job")
    app.register_blueprint(RESTful, url_prefix="/RESTful")
    app.register_blueprint(uploads, url_prefix="/uploads")
    app.register_blueprint(user, url_prefix="/user")
    mail.init_app(app)
    @app.route('/')
    def index():
        return render_template('index.html')
    from . import db
    db.init_app(app)

    @app.cli.command("set-admin")
    @click.argument("userid")
    def set_admin(userid):
        click.echo(userid)
        click.echo(db.get_db().assign_role(userid,"admin"))
    return app