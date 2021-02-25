from flask import Blueprint, request, render_template, redirect, url_for, session
from elice_library.models import User, Book, BookRental
from elice_library import db
from datetime import datetime

rental_bp = Blueprint('rental', __name__)


@rental_bp.route('/books-rental', methods=('GET', 'POST'))
def books_rental():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()

    if request.method == 'POST':
        book_id = request.form.get('book')

        book = Book.query.filter_by(id=book_id).first()

        stock = book.stock_num
        if stock >= 1:
            book.stock_num -= 1
            rental_info = BookRental(user=user, book=book)
            book.rental_set.append(rental_info)
            user.rental_set.append(rental_info)

            db.session.add(rental_info)
            db.session.commit()
            return redirect(url_for('main.index'))
        return redirect(url_for('main.index'))
    return render_template('rental/books_rental.html', rental_infos=user.rental_set)


@rental_bp.route('/books-return', methods=('GET', 'POST'))
def books_return():
    user_id = session['user_id']
    user = User.query.filter_by(id=user_id).first()

    if request.method == 'POST':
        book_id = request.form.get('book')
        book = Book.query.filter_by(id=book_id).first()
        book.stock_num += 1
        rental_info = BookRental.query.filter_by(user=user, book=book).first()
        rental_info.returned_at = datetime.now()
        db.session.commit()
        return redirect(url_for('rental.books_rental'))
    rental_infos = [info for info in user.rental_set if not info.returned_at]
    return render_template('rental/books_return.html', rental_infos=rental_infos)
