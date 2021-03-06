from datetime import datetime
from flask import g, request, render_template, redirect, url_for, session, make_response
from flask_restx import Namespace
from marshmallow import ValidationError
from elice_library.services.user_service import UserService
from elice_library.services.book_service import BookService
from elice_library.services.book_rental_service import BookRentalService
from elice_library.controllers.auth_controller import Resource
from elice_library.utils.errors import BooksAllRentedError, BookAlreadyRentedError


api = Namespace("rental", decription="rental related opertations")

user_service = UserService()
book_service = BookService()
book_rental_service = BookRentalService()


@api.route("/books-rental")
class BookRental(Resource):
    def get(self):
        return make_response(
            render_template(
                "rental/books_rental.html",
                rental_list=book_rental_service.get_rental_list_by(g.user.id),
            )
        )

    def post(self):
        try:
            json_data = request.get_json()
            book_id = json_data["book_id"]

            book_rental_service.start_rent(g.user.id, book_id)

        except BookAlreadyRentedError as e:
            return {"message": e.message}, 400
        except BooksAllRentedError as e:
            return {"message": e.message}, 400

        return {"message": f'"{book_service.find_by_id(book_id).book_name}"을(를) 빌렸습니다.'}


@api.route("/books-return")
class BookReturn(Resource):
    def get(self):
        not_finished = book_rental_service.find_not_finished_by_user_id(g.user.id)
        return make_response(
            render_template("rental/books_return.html", rental_list=not_finished)
        )

    def post(self):
        book_id = request.form.get("book_id")
        book_rental_service.finish_rent(g.user.id, book_id)
        return redirect(url_for("api.rental_book_rental"))


@api.route("/rental-best")
class RentalBest(Resource):
    def get(self):
        return make_response(
            render_template(
                "rental/rental_best.html", books=book_service.sort_by_rentals_num()
            )
        )
