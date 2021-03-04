import re
from marshmallow import Schema, INCLUDE, fields, ValidationError, validates, validate
from elice_library.database.config import ma
from elice_library.utils.errors import REQUIRED_INPUT_DATA, INVALID_USERNAME, INVALID_EMAIL, INVALID_PASSWORD, InvalidUsernameError, InvalidPasswordError


def not_allow_blank(data):
    if not data:
        raise ValidationError(REQUIRED_INPUT_DATA)


class UserCreateSchema(ma.Schema):
    class Meta:
        unknown = INCLUDE
        ordered = True

    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=not_allow_blank)
    email = fields.Email(required=True, validate=not_allow_blank, error_messages={'invalid': INVALID_EMAIL})
    password = fields.Str(required=True, validate=not_allow_blank, load_only=True)
    joined_at = fields.DateTime(dump_only=True)

    @validates("username")
    def validate_username(self, name):
        # 이름은 한글 또는 영문으로만 입력받는다
        if re.search(r'[^가-힣a-zA-Z]', name):
            raise ValidationError(INVALID_USERNAME)

    @validates("password")
    def validate_password(self, password):
        # 비밀번호는 영문, 숫자, 특수문자 3종류 이상을 조합하여
        # 최소 8자리 이상의 길이로 구성한다.
        if not re.fullmatch(r'^(?=.*[a-zA-Z])(?=.*\d)(?=.*[@$!%*#?&])[a-zA-Z\d@$!#%*?&]{8,}$', password):
            raise ValidationError(INVALID_PASSWORD)


class UserLoginSchema(ma.Schema):
    email = fields.Email(required=True, validate=not_allow_blank, error_messages={'invalid': INVALID_EMAIL})
    password = fields.Str(required=True, validate=not_allow_blank, load_only=True)
