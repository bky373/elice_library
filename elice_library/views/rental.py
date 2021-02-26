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
        book = Book.filter_by_id(book_id)

        if book.has_stock and not BookRental.query.filter_by(user_id=user_id, book_id=book_id).first():
            BookRental.create(user, book)
            return redirect(url_for('main.index'))
    return render_template('rental/books_rental.html', rental_infos=user.rental_set)


@rental_bp.route('/books-return', methods=('GET', 'POST'))
def book_return():
    user_id = session['user_id']
    user = User.find_by_id(user_id)

    if request.method == 'POST':
        book_id = request.form.get('book')
        book = Book.filter_by_id(book_id)

        book.add_stock()

        rental = BookRental.query.filter_by(user=user, book=book).first()
        rental.set_return_date()

        db.session.commit()
        return redirect(url_for('rental.book_rental'))
    rental_infos = [rental for rental in user.rental_set if not rental.is_returned]
    return render_template('rental/books_return.html', rental_infos=rental_infos)
