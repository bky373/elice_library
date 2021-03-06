from datetime import datetime
from flask import g, request, render_template, redirect, url_for, session, make_response
from flask_restx import Namespace
from marshmallow import ValidationError
from elice_library.services.book_service import (
    get_book_by_id,
    sort_books_by_rentals_num,
)
from elice_library.services.book_rental_service import (
    start_rent,
    finish_rent,
    get_unfinished_rentals_by_user_id,
    get_rentals_by_user_id,
)
from elice_library.controllers.auth_controller import Resource
from elice_library.utils.errors import BooksAllRentedError, BookAlreadyRentedError


api = Namespace("rental", decription="rental related opertations")


@api.route("/books-rental")
class BookRental(Resource):
    def get(self):
        return make_response(
            render_template(
                "rental/books_rental.html",
                rental_list=get_rentals_by_user_id(g.user.id),
            )
        )

    def post(self):
        try:
            json_data = request.get_json()
            book_id = json_data["book_id"]

            start_rent(g.user.id, book_id)

        except BookAlreadyRentedError as e:
            return {"message": e.message}, 400
        except BooksAllRentedError as e:
            return {"message": e.message}, 400

        return {"message": f'"{get_book_by_id(book_id).book_name}"을(를) 빌렸습니다.'}


@api.route("/books-return")
class BookReturn(Resource):
    def get(self):
        unfinished = get_unfinished_rentals_by_user_id(g.user.id)
        return make_response(
            render_template("rental/books_return.html", rental_list=unfinished)
        )

    def post(self):
        book_id = request.form.get("book_id")
        finish_rent(g.user.id, book_id)
        return redirect(url_for("api.rental_book_rental"))


@api.route("/rental-best")
class RentalBest(Resource):
    def get(self):
        return make_response(
            render_template(
                "rental/rental_best.html", books=sort_books_by_rentals_num()
            )
        )
