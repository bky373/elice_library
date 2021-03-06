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


class UserService:
    def find_by_id(self, user_id) -> User:
        return User.query.filter_by(id=user_id).first()

    def find_by_email(self, email) -> User:
        return User.query.filter_by(email=email).first()

    def register_user(self, username, email, password, re_password) -> User:
        existed = self.find_by_email(email)
        if existed:
            raise AccountAlreadyExistError()

        if not re_password:
            raise RePasswordRequiredError()

        if password != re_password:
            raise PasswordsNotMatchError()

        user = User.create(username, email, password)
        self.save_to_db(user)
        return user

    def login(self, email, password) -> User:
        existed = self.find_by_email(email)
        if not existed:
            raise AccountNotExistError()

        if not existed.check_password(password):
            raise PasswordsNotMatchError()

        return existed

    def save_to_db(self, user) -> None:
        db.session.add(user)
        db.session.commit()
