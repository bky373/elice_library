from typing import List
from marshmallow import ValidationError
from elice_library.database.config import db
from elice_library.domain.models.user import User
from elice_library.utils.error_messages import REQUIRED_INPUT_DATA, PASSWORDS_DO_NOT_MATCH, ALREADY_EXIST_ACCOUNT, DOESNT_EXIST_ACCOUNT, WRONG_PASSWORD_PROVIDED


class UserService:
    def find_by_id(self, user_id) -> User:
        return User.query.filter_by(id=user_id).first()
    
    def find_by_email(self, email) -> User:
        return User.query.filter_by(email=email).first()

    def sign_up(self, username, email, password, re_password) -> User:
        existed = self.find_by_email(email)
        if existed:
            raise ValidationError(ALREADY_EXIST_ACCOUNT)
        
        if not re_password:
            raise ValidationError(REQUIRED_INPUT_DATA) 
        if password != re_password:
            raise ValidationError(PASSWORDS_DO_NOT_MATCH) 

        user = User.create(username, email, password)
        self.save_to_db(user)
        return user

    def login(self, email, password) -> User:
        existed = self.find_by_email(email)
        if not existed:
            raise ValidationError(DOESNT_EXIST_ACCOUNT)

        if not existed.check_password(password):
            raise ValidationError(WRONG_PASSWORD_PROVIDED)
            
        return existed

    def save_to_db(self, user) -> None:
        db.session.add(user)
        db.session.commit()
