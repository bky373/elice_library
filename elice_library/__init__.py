from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()
migrate = Migrate()


def register_blueprints(app):
    from .views.main import main_bp
    from .views.auth import auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)

    from . import models

    register_blueprints(app)

    return app
