REQUIRED_INPUT_DATA = '필수 입력 항목입니다. 내용을 입력해주세요.'
INVALID_USERNAME = '이름은 한글 또는 영문으로만 입력해 주세요.'
INVALID_EMAIL = '올바른 이메일 형식이 아닙니다.'
INVALID_PASSWORD = '영문, 숫자, 특수문자를 조합하여 최소 8자리 이상의 길이로 구성해주세요.'
PASSWORDS_DO_NOT_MATCH = '비밀번호가 일치하지 않습니다.'
ACCOUNT_ALREADY_EXIST = '이미 등록된 계정입니다.'
ACCOUNT_DOESNT_EXIST = '존재하지 않는 계정입니다.'


class Error(Exception):
    pass


class RequiredInputDataError(Error):
    def __init__(self, message=REQUIRED_INPUT_DATA):
        self.message = message
        super().__init__(message)


class InvalidUsernameError(Error):
    def __init__(self, message=INVALID_USERNAME):
        self.message = message
        super().__init__(message)


class InvalidPasswordError(Error):
    def __init__(self, message=INVALID_USERNAME):
        self.message = message
        super().__init__(message)


class RePasswordRequiredError(Error):
    def __init__(self, message=REQUIRED_INPUT_DATA):
        self.message = message
        super().__init__(message)


class PasswordsNotMatchError(Error):
    def __init__(self, message=PASSWORDS_DO_NOT_MATCH):
        self.message = message
        super().__init__(message)


class AccountAlreadyExistError(Error):
    def __init__(self, message=ACCOUNT_ALREADY_EXIST):
        self.message = message
        super().__init__(message)


class AccountNotExistError(Error):
    def __init__(self, message=ACCOUNT_DOESNT_EXIST):
        self.message = message
        super().__init__(message)
