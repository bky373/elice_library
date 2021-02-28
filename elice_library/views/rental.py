from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, session
from elice_library import db
from elice_library.database.models.user import User
from elice_library.database.models.book import Book
from elice_library.database.models.book_rental import BookRental
from elice_library.utils.error_messages import BOOK_ALL_RENTED, BOOK_ALREADY_RENTED

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
            return {'message' : BOOK_ALL_RENTED}, 400
            
        rental = BookRental.find_last_by_ids(user_id, book_id)
        if rental is not None and not rental.has_finished:
            return {'message' : BOOK_ALREADY_RENTED}, 400

        rental = BookRental.create(user, book)
        if rental:
            user.add_rental_info(rental)
            book.add_rental_info(rental)    
            book.reduce_stock()
        return {'message' : f'"{book.book_name}"을(를) 빌렸습니다.'}
    return render_template('rental/books_rental.html', rental_list=user.rental_list)


@rental_bp.route('/books-return', methods=('GET', 'POST'))
def book_return():
    user_id = session['user_id']
    user = User.find_by_id(user_id)

    if request.method == 'POST':
        book_id = request.form.get('book')
        book = Book.find_by_id(book_id)

        book.add_stock()

        rental = BookRental.find_last_by_ids(user_id, book_id)
        rental.save_return_date()

        return redirect(url_for('rental.book_rental'))
    unfinished_rentals = [rental for rental in user.rental_list if not rental.has_finished]
    return render_template('rental/books_return.html', rental_list=unfinished_rentals)
