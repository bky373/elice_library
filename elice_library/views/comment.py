import logging
from datetime import datetime
from flask import Blueprint, request, render_template, redirect, url_for, session
from marshmallow import ValidationError
from elice_library import db
from elice_library.database.models.user import User
from elice_library.database.models.comment import Comment
from elice_library.database.models.comment import CommentSchema
from elice_library.services.book_service import BookService
from elice_library.utils.error_messages import COMMENT_REQUIRED, GIVE_SCORE_TO_BOOK


comment_bp = Blueprint('comment', __name__, url_prefix='/comment')
comment_schema = CommentSchema(many=True)
book_service = BookService()

@comment_bp.route('/', methods=('POST', ))
def comment_detail():
    data = request.get_json()
    content, rating, book_id = data['content'], data['rating'], data['book_id']

    if not content: return {'message': COMMENT_REQUIRED}, 400   
    if not rating: return {'message': GIVE_SCORE_TO_BOOK}, 400    

    user_id = session['user_id']
    user = User.find_by_id(user_id)
    book = book_service.find_by_id(book_id)
    
    # comment가 정상적으로 생성되면
    comment = Comment.create(user, book, content, rating)
    if comment:             
        book.update_rating()
    return {'comments' : comment_schema.dump(book.comments)}


@comment_bp.route('/comment-best')
def comment_best():
    return render_template('comment/comment_best.html', books=book_service.sort_by_comments_num())