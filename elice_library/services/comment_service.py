from typing import List
from marshmallow import ValidationError
from elice_library.database.config import db
from elice_library.domain.models.book import Book
from elice_library.domain.models.comment import Comment
from elice_library.services.user_service import get_user_by_id
from elice_library.services.book_service import get_book_by_id
from elice_library.utils.errors import (
    COMMENT_REQUIRED,
    SCORE_REQUIRED,
    CommentAlreadyPostedError,
)


def get_comment_by_id(comment_id) -> Comment:
    return Comment.query.filter_by(id=comment_id).first()


def get_comments_by_user(user) -> List[Comment]:
    return Comment.query.filter_by(user=user).all()


def get_books_commented_by_user(user) -> List[Book]:
    comments = get_comments_by_user(user)
    return [comment.book for comment in comments]


def get_comment_by_userid_and_bookid(user_id, book_id) -> Comment:
    return Comment.query.filter_by(user_id=user_id, book_id=book_id).first()


def create_comment(user_id, book_id, content, rating) -> Comment:
    user = get_user_by_id(user_id)
    book = get_book_by_id(book_id)

    existed = get_comment_by_userid_and_bookid(user_id, book_id)
    if existed:
        raise CommentAlreadyPostedError()

    if not content:
        raise ValidationError(COMMENT_REQUIRED)
    if not rating:
        raise ValidationError(SCORE_REQUIRED)

    comment = Comment.create(user, book, content, rating)
    book.update_rating()

    save_to_db(comment)
    return comment


def get_comments_by_book_id(book_id) -> List[Comment]:
    book = get_book_by_id(book_id)
    return book.comments


def update_comment(comment_id, content) -> Comment:
    if not content:
        raise ValidationError(COMMENT_REQUIRED)

    comment = get_comment_by_id(comment_id)
    comment.update(content)
    save_to_db(comment)
    return comment


def delete_comment(comment_id) -> None:
    comment = get_comment_by_id(comment_id)

    # delete를 먼저 해주어야 book의 comment 개수가 1 줄어들어 
    # 올바른 평점 계산이 된다.
    db.session.delete(comment)
    comment.book.update_rating()

    db.session.commit()


def save_to_db(user) -> None:
    db.session.add(user)
    db.session.commit()
