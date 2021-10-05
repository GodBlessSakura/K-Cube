from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from app.config import config
from app.blueprints.course import course
from app.blueprints.job import job
from app.blueprints.RESTful import RESTful
from app.blueprints.uploads import uploads
from app.blueprints.user import user
bootstrap = Bootstrap()
mail = Mail()


def create_app(config_object):
    app = Flask(__name__)
    if config_object is None:
        config_object == config['default']
    app.config.from_object(config_object)

    app.register_blueprint(course)
    app.register_blueprint(job, url_prefix="/job")
    app.register_blueprint(RESTful, url_prefix="/RESTful")
    app.register_blueprint(uploads, url_prefix="/uploads")
    app.register_blueprint(user, url_prefix="/user")
    bootstrap.init_app(app)
    mail.init_app(app)
    return app