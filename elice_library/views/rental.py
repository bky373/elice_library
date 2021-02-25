from flask import Blueprint, request, render_template, redirect, url_for, session
from elice_library.models import User, Book, BookRental
from elice_library import db

rental_bp = Blueprint('rental', __name__, url_prefix='/rental')


@rental_bp.route('/', methods=('GET', 'POST' ))
def info():
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
    return render_template('rental/rental_info.html', rental_infos=user.rental_set)

