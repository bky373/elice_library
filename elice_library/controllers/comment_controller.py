from flask import request, g, render_template, redirect, url_for, session, make_response
from flask_restx import Namespace
from marshmallow import ValidationError
from elice_library.domain.schemas.comment_schema import CommentSchema
from elice_library.services.book_service import sort_books_by_comments_num
from elice_library.services.comment_service import (
    create_comment,
    update_comment,
    delete_comment,
    get_comments_by_book_id,
)
from elice_library.controllers.auth_controller import Resource
from elice_library.utils.errors import (
    CommentAlreadyPostedError,
    CommentNotExistError,
    COMMENT_DELETE_FAIL,
    COMMENT_UPDATE_FAIL,
)


api = Namespace("comment", description="comment related operations")

comment_schema = CommentSchema(many=True)

COMMENT_UPDATE_SUCCESS = "댓글을 수정하였습니다."
COMMENT_DELETE_SUCCESS = "댓글을 삭제하였습니다."


@api.route("/")
class Comment(Resource):
    @api.doc("create a new comment")
    def post(self):
        try:
            data = request.get_json()
            content, rating, book_id = data["content"], data["rating"], data["book_id"]

            create_comment(g.user.id, book_id, content, rating)

        except CommentAlreadyPostedError as e:
            return {"message": e.message}, 400
        except ValidationError as e:
            return {"message": e.messages}, 400

        return {"comments": comment_schema.dump(get_comments_by_book_id(book_id))}

    @api.doc("update the selected comment")
    def put(self):
        try:
            data = request.get_json()
            comment_id, content = data["comment_id"], data["content"]

            update_comment(comment_id, content)

        except CommentNotExistError as e:
            return {"message": e.message}, 400
        except ValidationError as e:
            return {"message": e.messages}, 400
        except Exception as e:
            return {"message": COMMENT_UPDATE_FAIL}, 400

        return {"message": COMMENT_UPDATE_SUCCESS}

    @api.doc("delete the selected comment")
    def delete(self):
        try:
            data = request.get_json()
            comment_id = data["comment_id"]

            delete_comment(comment_id)

        except CommentNotExistError as e:
            return {"message": e.message}, 400
        except Exception:
            return {"message": COMMENT_DELETE_FAIL}, 400

        return {"message": COMMENT_DELETE_SUCCESS}


@api.route("/comment-best")
class CommentBest(Resource):
    @api.doc("show books sorted by number of comments in descending order")
    def get(self):
        return make_response(
            render_template(
                "comment/comment_best.html", books=sort_books_by_comments_num()
            )
        )
