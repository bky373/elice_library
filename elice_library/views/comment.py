from flask import Blueprint, request, render_template, redirect, url_for, session
from marshmallow import ValidationError
from elice_library.domain.schemas.comment_schema import CommentSchema
from elice_library.services.user_service import UserService
from elice_library.services.book_service import BookService
from elice_library.services.comment_service import CommentService
from elice_library.utils.errors import CommentAlreadyPostedError, CommentNotExistError, COMMENT_DELETE_FAIL, COMMENT_UPDATE_FAIL

comment_bp = Blueprint('comment', __name__, url_prefix='/comment')

comment_schema = CommentSchema(many=True)
user_service = UserService()
book_service = BookService()
comment_service = CommentService()

COMMENT_UPDATE_SUCCESS = '댓글을 수정하였습니다.'
COMMENT_DELETE_SUCCESS = '댓글을 삭제하였습니다.'


@comment_bp.route('/', methods=('POST', 'PUT', 'DELETE'))
def comment_detail():
    if request.method == 'POST':
        try:
            data = request.get_json()
            content, rating, book_id = data['content'], data['rating'], data['book_id']

            user_id = session['user_id']

            comment_service.create_comment(user_id, book_id, content, rating)

        except CommentAlreadyPostedError as e:
            return {'message': e.message}, 400
        except ValidationError as e:
            return {'message': e.messages}, 400
        return {'comments': comment_schema.dump(comment_service.get_comments_by(book_id))}

    elif request.method == 'PUT':
        try:
            data = request.get_json()
            comment_id, content = data['comment_id'], data['content']
            comment_service.update_comment(comment_id, content)

        except CommentNotExistError as e:
            return {'message': e.message}, 400
        except ValidationError as e:
            return {'message': e.messages}, 400
        except Exception as e:
            return {'message': COMMENT_UPDATE_FAIL}, 400

        return {'message' : COMMENT_UPDATE_SUCCESS}

    elif request.method == 'DELETE':
        try:
            data = request.get_json()
            comment_id = data['comment_id']

            comment_service.delete_comment(comment_id)

        except CommentNotExistError as e:
            return {'message': e.message}, 400
        except Exception:
            return {'message': COMMENT_DELETE_FAIL}, 400

        return {'message': COMMENT_DELETE_SUCCESS}


@comment_bp.route('/comment-best')
def comment_best():
    return render_template('comment/comment_best.html', books=book_service.sort_by_comments_num())
