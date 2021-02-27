from .utils import config
from flask import Flask
from elice_library.database.config import db, migrate, ma


def register_blueprints(app):
    from .views.main import main_bp
    from .views.auth import auth_bp
    from .views.books import books_bp
    from .views.rental import rental_bp
    from .views.comment import comment_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(rental_bp)
    app.register_blueprint(comment_bp)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .database.models import user, book, book_rental, comment

    register_blueprints(app)

    return app
