from typing import List
from marshmallow import ValidationError
from elice_library.database.config import db
from elice_library.domain.models.comment import Comment
from elice_library.services.user_service import UserService
from elice_library.services.book_service import BookService
from elice_library.utils.errors import COMMENT_REQUIRED, SCORE_REQUIRED, CommentAlreadyPostedError


class CommentService:
    user_service = UserService()
    book_service = BookService()

    def find_by_ids(self, user_id, book_id) -> Comment:
        return Comment.query.filter_by(user_id=user_id, book_id=book_id).first()

    def add_comment(self, user_id, book_id, content, rating) -> Comment:
        user = self.user_service.find_by_id(user_id)
        book = self.book_service.find_by_id(book_id)
        
        existed = self.find_by_ids(user_id, book_id)
        if existed:
            raise CommentAlreadyPostedError()

        if not content:
            raise ValidationError(COMMENT_REQUIRED)
        if not rating:
            raise ValidationError(SCORE_REQUIRED)
        
        comment = Comment.create(user, book, content, rating)
        book.update_rating()

        self.save_to_db(comment)
        return comment

    def get_comments_by(self, book_id) -> List[Comment]:
        book = self.book_service.find_by_id(book_id)
        return book.comments

    def save_to_db(self, user) -> None:
        db.session.add(user)
        db.session.commit()

        