import os

# basedir = os.path.abspath(".")
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    BOOTSTRAP_SERVE_LOCAL = True
    SECRET_KEY = "Hard to guess string"
    DATABASE_ADDRESS = "bolt://127.0.0.1:7687"
    DATABASE = "neo4j"
    DATABASE_PASSWORD = "1234"
    requireUserVerification = True

class standaloneConfig(Config):
    requireUserVerification = False


class DevelopmentConfig(Config):
    DEBUG = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True


class ProductionConfig(Config):
    TESTING = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "productin": ProductionConfig,
    "default": DevelopmentConfig,
    "standalone": standaloneConfig
}
