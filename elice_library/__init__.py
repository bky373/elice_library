from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import config

db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()

def register_blueprints(app):
    from .views.main import main_bp
    from .views.auth import auth_bp
    from .views.books import books_bp
    from .views.rental import rental_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(rental_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    
    from . import models

    register_blueprints(app)

    return app
