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

        user = User.find_by_id(user_id)
        book = Book.find_by_id(book_id)

        content = request.form.get('content')
        rating = request.form.get('rating')
        
        # 평점이 0 점이면,
        if not rating: return {'message': 'No rating value provided'}
        
        # comment가 정상적으로 생성되면
        comment = Comment.create(user, book, content, rating)
        if comment:             
            user.add_comment(comment)
            book.add_comment(comment)
            book.update_rating()
        return redirect(url_for('books.book_detail', book_id=book.id))
    return redirect(url_for('main.index'))
