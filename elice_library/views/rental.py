from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, session
from marshmallow import ValidationError
from elice_library import db
from elice_library.database.models.user import User
from elice_library.services.book_service import BookService
from elice_library.utils.error_messages import BOOK_ALL_RENTED
from elice_library.services.book_rental_service import BookRentalService


rental_bp = Blueprint('rental', __name__)
book_service = BookService()
book_rental_service = BookRentalService()

@rental_bp.route('/books-rental', methods=('GET', 'POST'))
def book_rental():
    user_id = session['user_id']
    user = User.find_by_id(user_id)

    if request.method == 'POST':
        json_data = request.get_json()
        book_id = json_data['book_id']

        book = book_service.find_by_id(book_id)

        try:
            book_rental_service.start_rent(user, book)
        except ValidationError as e:
            return {'message' : e.messages}, 400

        return {'message': f'"{book.book_name}"을(를) 빌렸습니다.'}
    return render_template('rental/books_rental.html', rental_list=user.rental_list)


@rental_bp.route('/books-return', methods=('GET', 'POST'))
def book_return():
    user_id = session['user_id']

    if request.method == 'POST':
        book_id = request.form.get('book')

        book_rental_service.finish_rent(user_id, book_id)
        return redirect(url_for('rental.book_rental'))
        
    not_finished = book_rental_service.find_not_finished_by_user_id(user_id)
    return render_template('rental/books_return.html', rental_list=not_finished)


@rental_bp.route('/rental-best')
def rental_best():
    return render_template('rental/rental_best.html', books=book_service.sort_by_rentals_num())
