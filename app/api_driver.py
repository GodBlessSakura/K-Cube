from app.neoDB import APIDriver

from flask import current_app, g


def get_api_driver() -> APIDriver:
    if "api_driver" not in g:
        g.api_driver = APIDriver("bolt://localhost:7687", "neo4j", "1234")
    return g.api_driver


def init_app(app):
    app.teardown_appcontext(close_api_driver)


def close_api_driver(e=None):
    api_driver = g.pop("api_driver", None)

    if api_driver is not None:
        api_driver.close()
