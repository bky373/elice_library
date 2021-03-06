REQUIRED_INPUT_DATA = "필수 입력 항목입니다. 내용을 입력해주세요."
INVALID_USERNAME = "이름은 한글 또는 영문으로만 입력해 주세요."
INVALID_EMAIL = "올바른 이메일 형식이 아닙니다."
INVALID_PASSWORD = "영문, 숫자, 특수문자를 조합하여 최소 8자리 이상의 길이로 구성해주세요."
INVALID_NEW_PASSWORD = "현재 비밀번호와 다른 비밀번호를 입력해주세요."
PASSWORDS_DO_NOT_MATCH = "비밀번호가 일치하지 않습니다."
ACCOUNT_ALREADY_EXIST = "이미 등록된 계정입니다."
ACCOUNT_DOESNT_EXIST = "존재하지 않는 계정입니다."

BOOKS_ALL_RENTED = "책이 모두 대여 중입니다."
BOOK_ALREADY_RENTED = "책을 이미 대여하였습니다."

COMMENT_REQUIRED = "댓글 칸을 채워주세요 :)"
SCORE_REQUIRED = "책에 대한 별 점수를 매겨주세요 :)"
COMMENT_ALREADY_POSTED = "댓글을 이미 작성하였습니다 :)"
COMMENT_NOT_EXIST = "해당하는 댓글이 없습니다"
COMMENT_DELETE_FAIL = "댓글 삭제에 실패했습니다."
COMMENT_UPDATE_FAIL = "댓글 수정에 실패했습니다"


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


class InvalidNewPasswordError(Error):
    def __init__(self, message=INVALID_NEW_PASSWORD):
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


class BookAlreadyRentedError(Error):
    def __init__(self, message=BOOK_ALREADY_RENTED):
        self.message = message
        super().__init__(message)


class BooksAllRentedError(Error):
    def __init__(self, message=BOOKS_ALL_RENTED):
        self.message = message
        super().__init__(message)


class CommentAlreadyPostedError(Error):
    def __init__(self, message=COMMENT_ALREADY_POSTED):
        self.message = message
        super().__init__(message)


class CommentNotExistError(Error):
    def __init__(self, message=COMMENT_NOT_EXIST):
        self.message = message
        super().__init__(message)
