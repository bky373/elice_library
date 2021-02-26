
from elice_library.database.config import db, ma
from marshmallow import Schema, INCLUDE, fields, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from pytz import timezone


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    joined_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.now(timezone('Asia/Seoul')))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided')


class UserCreateSchema(ma.Schema):
    class Meta:
        unknown = INCLUDE

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=must_not_be_blank, error_messages={
                          'required': 'Username required'})
    email = fields.Email(required=True, validate=must_not_be_blank, error_messages={
                         'required': 'Email required'})
    password = fields.Str(load_only=True, required=True, validate=must_not_be_blank, error_messages={
                          'required': 'Password required'})
    joined_at = fields.DateTime(dump_only=True)


class UserLoginSchema(ma.Schema):
    email = fields.Email(required=True, validate=must_not_be_blank, error_messages={
                         'required': 'Email required'})
    password = fields.Str(load_only=True, required=True, validate=must_not_be_blank, error_messages={
                          'required': 'Password required'})
