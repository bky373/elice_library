import logging
from datetime import datetime
from elice_library import db
from elice_library.database.models.user import User
from elice_library.database.models.comment import Comment
from elice_library.database.models.comment import CommentSchema
from elice_library.services.book_service import BookService
from flask import Blueprint, request, render_template, redirect, url_for, session
from elice_library.utils.error_messages import COMMENT_REQUIRED, GIVE_SCORE_TO_BOOK
from marshmallow import ValidationError


comment_bp = Blueprint('comment', __name__, url_prefix='/comment')
comment_schema = CommentSchema(many=True)

@comment_bp.route('/', methods=('POST', ))
def comment_detail():
    data = request.get_json()
    content, rating, book_id = data['content'], data['rating'], data['book_id']

    if not content: return {'message': COMMENT_REQUIRED}, 400   
    if not rating: return {'message': GIVE_SCORE_TO_BOOK}, 400    

    user_id = session['user_id']
    user = User.find_by_id(user_id)
    book = BookService.find_by_id(book_id)
    
    # comment가 정상적으로 생성되면
    comment = Comment.create(user, book, content, rating)
    if comment:             
        book.update_rating()
    return {'comments' : comment_schema.dump(book.comments)}


@comment_bp.route('/comment-best')
def comment_best():
    return render_template('comment/comment_best.html', books=BookService.sort_by_comments_num())