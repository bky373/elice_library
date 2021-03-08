from flask import request, g, session, redirect, render_template, url_for, make_response
from flask_restx import Namespace
from marshmallow import ValidationError
from elice_library.domain.schemas.user_schema import (
    UserCreateSchema,
    UserWithdrawalSchema,
)
from elice_library.services.user_service import (
    get_books_marked_by_user,
    get_books_voted_by_user,
    update_user_password,
    deactivate_user,
)
from elice_library.services.comment_service import get_books_commented_by_user
from elice_library.controllers.auth_controller import Resource
from elice_library.utils.errors import (
    AccountNotExistError,
    InvalidNewPasswordError,
    PasswordsNotMatchError,
    RePasswordRequiredError,
)


api = Namespace("user", description="user related operations")
user_create_schema = UserCreateSchema()
user_withdrawal_schema = UserWithdrawalSchema()


@api.route("/marked-books")
class UserBookmarks(Resource):
    @api.doc("show books marked by user logged in")
    def get(self):
        return make_response(
            render_template(
                "user/marked_books.html", books=get_books_marked_by_user(g.user)
            )
        )


@api.route("/voted-books")
class UserVoteBooks(Resource):
    @api.doc("show books voted by user logged in")
    def get(self):
        return make_response(
            render_template(
                "user/voted_books.html", books=get_books_voted_by_user(g.user)
            )
        )


@api.route("/commented-books")
class UserCommentBooks(Resource):
    @api.doc("show books commented by user logged in")
    def get(self):
        return make_response(
            render_template(
                "user/commented_books.html", books=get_books_commented_by_user(g.user)
            )
        )


@api.route("/new-password")
class NewPassword(Resource):
    @api.doc("show a page where user can update a password")
    def get(self):
        return make_response(render_template("user/new_password.html"))

    @api.doc("update a password")
    def post(self):
        try:
            json_data = request.get_json()
            data = user_create_schema.load(json_data, partial=True)

            password, re_password = (
                data["password"],
                data["repassword"],
            )

            user = update_user_password(g.user, password, re_password)
            session.pop("user_id", None)

        except ValidationError as e:
            return e.messages, 400
        except InvalidNewPasswordError as e:
            return {"password": e.message}, 400
        except AccountNotExistError as e:
            return {"email": e.message}, 400
        except RePasswordRequiredError as e:
            return {"repassword": e.message}, 400
        except PasswordsNotMatchError as e:
            return {"repassword": e.message}, 400

        return {"username": user.username}, 201


@api.route("/withdrawal")
class UserWithdrawal(Resource):
    @api.doc("show user withdrawal form")
    def get(self):
        return make_response(render_template("user/withdrawal.html"))

    @api.doc("deactivate user")
    def post(self):
        try:
            json_data = request.get_json()
            data = user_withdrawal_schema.load(json_data)

            deactivate_user(g.user, data["password"])

            session.pop("user_id", None)

        except ValidationError as e:
            return e.messages, 400
        except AccountNotExistError as e:
            return {"email": e.message}, 400
        except PasswordsNotMatchError as e:
            return {"password": e.message}, 400

        return make_response(render_template("user/withdrawal.html"))
