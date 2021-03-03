from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, session
from marshmallow import ValidationError
from elice_library import db
from elice_library.database.models.user import User
from elice_library.database.models.book import Book
from elice_library.database.models.book_rental import BookRental
from elice_library.utils.error_messages import BOOK_ALL_RENTED
from elice_library.services.book_rental import BookRentalService

rental_bp = Blueprint('rental', __name__)


@rental_bp.route('/books-rental', methods=('GET', 'POST'))
def book_rental():
    user_id = session['user_id']
    user = User.find_by_id(user_id)

    if request.method == 'POST':
        json_data = request.get_json()

        book_id = json_data['book_id']
        book = Book.find_by_id(book_id)

        if not book.has_stock:
            return {'message': BOOK_ALL_RENTED}, 400

        try:
            rental = BookRentalService.create(user, book)
        except ValidationError as e:
            return {'message': e.messages}, 400

        if rental:
            book.reduce_stock()
        return {'message': f'"{book.book_name}"을(를) 빌렸습니다.'}
    return render_template('rental/books_rental.html', rental_list=user.rental_list)


@rental_bp.route('/books-return', methods=('GET', 'POST'))
def book_return():
    user_id = session['user_id']

    if request.method == 'POST':
        book_id = request.form.get('book')
        book = Book.find_by_id(book_id)

        book.add_stock()

        BookRentalService.finish_rental(user_id, book_id)

        return redirect(url_for('rental.book_rental'))
    not_finished_rentals = BookRentalService.find_not_finished_by_user_id(
        user_id)
    return render_template('rental/books_return.html', rental_list=not_finished_rentals)


@rental_bp.route('/rental-best')
def rental_best():
    return render_template('rental/rental_best.html', books=Book.sort_by_rentals_num())
