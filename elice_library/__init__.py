from .utils import config
from flask import Flask, Blueprint
from flask_restx import Api
from elice_library.routes import add_namespaces
from elice_library.database.config import db, migrate, ma


blueprint = Blueprint("api", __name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    api = Api(
        blueprint,
        title="ELICE LIBRARY WEB APPLICATION",
        description="library web service with flask restx apis",
    )

    add_namespaces(api)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .domain.models import user, book, book_rental, comment

    return app
