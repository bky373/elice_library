from flask import Blueprint, request, render_template, redirect, url_for, session
from marshmallow import ValidationError
from elice_library.domain.schemas.comment_schema import CommentSchema
from elice_library.services.user_service import UserService
from elice_library.services.book_service import BookService
from elice_library.services.comment_service import CommentService


comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

comment_schema = CommentSchema(many=True)
user_service = UserService()
book_service = BookService()
comment_service = CommentService()


@comment_bp.route('/', methods=('POST', ))
def comment_detail():
    try:
        data = request.get_json()
        content, rating, book_id = data['content'], data['rating'], data['book_id']

        user_id = session['user_id']
        
        comment_service.add_comment(user_id, book_id, content, rating)

    except ValidationError as e:
        return {'message' : e.messages}, 400
    return {'comments' : comment_schema.dump(comment_service.get_comments_by(book_id))}


@comment_bp.route('/comment-best')
def comment_best():
    return render_template('comment/comment_best.html', books=book_service.sort_by_comments_num())