import re
import logging
from elice_library.database.config import db, ma
from marshmallow import Schema, INCLUDE, fields, ValidationError, validates, validate
from marshmallow.validate import Length
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from pytz import timezone
from elice_library.utils.error_messages import REQUIRED_INPUT_DATA, INVALID_USERNAME, ALREADY_EXIST_ACCOUNT, INVALID_PASSWORD, DOESNT_EXIST_ACCOUNT

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    joined_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.joined_at = datetime.now(timezone('Asia/Seoul'))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_rental_info(self, rental):
        self.rental_list.append(rental)
        return self.rental_list

    def add_comment(self, comment):
        self.comments.append(comment)
        return self.comments

    def __repr__(self):
        return "<User(id='%s', name='%s', email='%s', password='%s', joined_at='%s')>" % (
            self.id, self.username, self.email, self.password, self.joined_at)

    @staticmethod
    def create(username, email, password):
        try:
            user = User(username=username, email=email, password=password)
            db.session.add(user)
            db.session.commit()
            return user
        # 이미 등록된 유저가 있을 때
        except IntegrityError as e:
            logging.warning(e)
            return None
        except Exception as e:
            logging.warning(e)
            return None

    @staticmethod
    def find_by_id(id):
        return User.query.filter_by(id=id).first()

    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()


def not_allow_blank(data):
    if not data: raise ValidationError(REQUIRED_INPUT_DATA)

class UserCreateSchema(ma.Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=not_allow_blank)
    email = fields.Email(required=True, validate=not_allow_blank)
    password = fields.Str(required=True, validate=not_allow_blank, load_only=True)
    joined_at = fields.DateTime(dump_only=True)

    @validates("username")
    def validate_username(self, name):
        if re.search(r'^(?![가-힣|a-z|A-Z]).', name):
            raise ValidationError(INVALID_USERNAME)
    
    @validates("email")
    def validate_email(self, email):
        if User.find_by_email(email):
            raise ValidationError(ALREADY_EXIST_ACCOUNT)

    @validates("password")
    def validate_password(self, password):
        if not re.fullmatch(r'^(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,}$', password):
            raise ValidationError(INVALID_PASSWORD)

class UserLoginSchema(ma.Schema):
    email = fields.Email(required=True, validate=not_allow_blank)
    password = fields.Str(required=True, validate=not_allow_blank, load_only=True)

    @validates("email")
    def validate_email(self, email):
        if not User.find_by_email(email):
            raise ValidationError(DOESNT_EXIST_ACCOUNT)
    