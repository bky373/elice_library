from flask import g, render_template, request, make_response
from flask_restx import Namespace
from elice_library.services.book_service import (
    paginate_books,
    recommend_book_by_user,
    get_book_by_id,
    sort_books_by_published_date,
    sort_books_by_rating,
)
from elice_library.controllers.auth_controller import Resource


api = Namespace("books", description="book related operations")

ITEMS_PER_PAGE = 8


@api.route("/")
class BookList(Resource):
    @api.doc("show paginated book list")
    def get(self):
        page = request.args.get("page", type=int, default=1)
        return make_response(
            render_template(
                "books/book_list.html",
                books=paginate_books(page, per_page=ITEMS_PER_PAGE),
            )
        )


@api.route("/<int:book_id>")
class Book(Resource):
    @api.doc("show detail of selected book")
    def get(self, book_id):
        return make_response(
            render_template("books/book_detail.html", book=get_book_by_id(book_id))
        )


@api.route("/")
class Recommend(Resource):
    @api.doc("add or cancel a recommendation")
    def post(self):
        data = request.get_json()
        book_id = data["book_id"]

        return {"message": recommend_book_by_user(g.user, book_id)}


@api.route("/new-arrivals")
class NewArrivals(Resource):
    @api.doc("show books sorted by published date in descending order")
    def get(self):
        return make_response(
            render_template(
                "books/new_arrivals.html", books=sort_books_by_published_date()
            )
        )


@api.route("/rating-best")
class RatingBest(Resource):
    @api.doc("show books sorted by rating in descending order")
    def get(self):
        return make_response(
            render_template("books/rating_best.html", books=sort_books_by_rating())
        )
