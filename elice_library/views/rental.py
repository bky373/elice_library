from flask import Blueprint, request, render_template, redirect, url_for, session
from elice_library.database.models.user import User
from elice_library.database.models.book import Book
from elice_library.database.models.book_rental import BookRental
from elice_library import db
from datetime import datetime

rental_bp = Blueprint('rental', __name__)


@rental_bp.route('/books-rental', methods=('GET', 'POST'))
def book_rental():
    user_id = session['user_id']
    user = User.find_by_id(user_id)

    if request.method == 'POST':
        book_id = request.form.get('book')
        book = Book.find_by_id(book_id)

        if book.has_stock and not BookRental.find_by_ids(user_id, book_id):
            BookRental.create(user, book)
            return redirect(url_for('main.index'))
    return render_template('rental/books_rental.html', rental_list=user.rental_list)


@rental_bp.route('/books-return', methods=('GET', 'POST'))
def book_return():
    user_id = session['user_id']
    user = User.find_by_id(user_id)

    if request.method == 'POST':
        book_id = request.form.get('book')
        book = Book.find_by_id(book_id)

        book.add_stock()

        rental = BookRental.find_by_ids(user_id, book_id)
        rental.save_return_date()

        return redirect(url_for('rental.book_rental'))
    unfinished_rentals = [rental for rental in user.rental_list if not rental.has_finished]
    return render_template('rental/books_return.html', rental_list=unfinished_rentals)
