from flask import request, g, session, redirect, render_template, url_for, make_response
from flask_restx import Namespace
from marshmallow import ValidationError
from elice_library.domain.schemas.user_schema import (
    UserCreateSchema,
    UserLoginSchema,
    UserWithdrawalSchema,
)
from elice_library.services.user_service import (
    deactivate_user,
    get_books_voted_by_user,
    get_books_marked_by_user,
)
from elice_library.controllers.auth_controller import Resource
from elice_library.utils.errors import AccountNotExistError, PasswordsNotMatchError


api = Namespace("user", description="user related operations")

user_withdrawal_schema = UserWithdrawalSchema()


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


@api.route("/voted-books")
class UserVoteBooks(Resource):
    @api.doc("show books voted by user logged in")
    def get(self):
        return make_response(
            render_template(
                "user/voted_books.html", books=get_books_voted_by_user(g.user)
            )
        )


@api.route("/marked-books")
class UserBookmarks(Resource):
    @api.doc("show books marked by user logged in")
    def get(self):
        return make_response(
            render_template(
                "user/marked_books.html", books=get_books_marked_by_user(g.user)
            )
        )
