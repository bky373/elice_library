from flask import redirect, url_for, make_response
from flask_restx import Namespace
from elice_library.domain.models.book import Book
from elice_library.controllers.auth_controller import Resource


api = Namespace("main", description="main related operations")


@api.route("/")
@api.route("/index")
class Index(Resource):
    def get(self):
        return redirect(url_for("api.books_book_list"))
