import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from config import Config

bootstrap = Bootstrap()
moment = Moment()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bootstrap.init_app(app)
    moment.init_app(app)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp)

    from app.sparql import bp as sparql_bp

    app.register_blueprint(sparql_bp)

    from app.trust import bp as trust_bp

    app.register_blueprint(trust_bp)

    from app.dua import bp as dua_bp

    app.register_blueprint(dua_bp)

    from app.policy import bp as policy_bp

    app.register_blueprint(policy_bp)

    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler(
        "logs/trusted_middleware.log", maxBytes=51200, backupCount=5
    )
    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]"
        )
    )
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info("Trusted Middleware Startup")

    return app


# source venv/bin/activate
