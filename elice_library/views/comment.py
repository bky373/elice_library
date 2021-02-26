from flask import Blueprint, request, render_template, redirect, url_for, session
from elice_library.database.models.user import User
from elice_library.database.models.book import Book
from elice_library.database.models.comment import Comment
from elice_library import db
from datetime import datetime

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

@comment_bp.route('/', methods=('GET', 'POST'))
def comment_detail():
    if request.method == 'POST':
        user_id = session['user_id']
        book_id = request.form.get('book')
        
        user = User.query.filter_by(id=user_id).first()
        book = Book.query.filter_by(id=book_id).first()
        content = request.form.get('content')
        rating = request.form.get('rating')

        comment = Comment.create(user, book, content, rating)
        if comment:
            return redirect(url_for('books.book_detail', book_id=book.id))
    return redirect(url_for('main.index'))
    