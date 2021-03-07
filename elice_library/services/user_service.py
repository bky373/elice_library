from typing import List
from marshmallow import ValidationError
from elice_library.database.config import db
from elice_library.domain.models.user import User
from elice_library.utils.errors import (
    AccountAlreadyExistError,
    RePasswordRequiredError,
    PasswordsNotMatchError,
    AccountNotExistError,
)


def get_user_by_id(user_id) -> User:
    return User.query.filter_by(id=user_id).first()


def get_user_by_email(email) -> User:
    return User.query.filter_by(email=email).first()


def register_user(username, email, password, re_password) -> User:
    existed = get_user_by_email(email)
    if existed:
        raise AccountAlreadyExistError()

    if not re_password:
        raise RePasswordRequiredError()

    if password != re_password:
        raise PasswordsNotMatchError()

    user = User.create(username, email, password)
    save_to_db(user)
    return user


def login_user(email, password) -> User:
    existed = get_user_by_email(email)
    if not existed or not existed.is_active:
        raise AccountNotExistError()

    if not existed.check_password(password):
        raise PasswordsNotMatchError()

    return existed


def deactivate_user(user, password) -> User:
    if not user.check_password(password):
        raise PasswordsNotMatchError()

    user.deactivate()
    save_to_db(user)
    return user


def save_to_db(user) -> None:
    db.session.add(user)
    db.session.commit()
