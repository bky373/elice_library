from flask import request, g, session, redirect, render_template, url_for, make_response
import flask_restx
from functools import wraps
from flask_restx import Namespace
from marshmallow import ValidationError
from elice_library.domain.schemas.user_schema import UserCreateSchema, UserLoginSchema
from elice_library.services.user_service import find_by_id, register_user, login_user
from elice_library.utils.errors import (
    AccountAlreadyExistError,
    RePasswordRequiredError,
    PasswordsNotMatchError,
    AccountNotExistError,
)


api = Namespace("auth", description="auth related operations")

user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()


def load_logged_in_user(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")
        g.user = find_by_id(user_id) if user_id else None
        return func(*args, **kwargs)

    return wrapper


class Resource(flask_restx.Resource):
    method_decorators = [load_logged_in_user]


@api.route("/signup")
class AuthSignUp(Resource):
    def get(self):
        return make_response(render_template("auth/signup.html"))

    def post(self):
        try:
            json_data = request.get_json()
            data = user_create_schema.load(json_data)

            username, email, password, re_password = (
                data["username"],
                data["email"],
                data["password"],
                data["repassword"],
            )

            user = register_user(
                username=username,
                email=email,
                password=password,
                re_password=re_password,
            )

        except ValidationError as e:
            return e.messages, 400
        except AccountAlreadyExistError as e:
            return {"email": e.message}, 400
        except RePasswordRequiredError as e:
            return {"repassword": e.message}, 400
        except PasswordsNotMatchError as e:
            return {"repassword": e.message}, 400

        return {"username": user.username}, 201


@api.route("/login")
class AuthLogin(Resource):
    def get(self):
        return make_response(render_template("auth/login.html"))

    def post(self):
        try:
            json_data = request.get_json()
            data = user_login_schema.load(json_data)

            email, password = data["email"], data["password"]

            user = login_user(email, password)

            session.pop("user_id", None)
            session["user_id"] = user.id

        except ValidationError as e:
            return e.messages, 400
        except AccountNotExistError as e:
            return {"email": e.message}, 400
        except PasswordsNotMatchError as e:
            return {"password": e.message}, 400

        return {"username": user.username}, 201


@api.route("/logout")
class AuthLogout(Resource):
    def get(self):
        session.pop("user_id", None)
        return redirect(url_for("api.main_index"))
