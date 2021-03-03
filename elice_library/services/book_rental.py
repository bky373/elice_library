import logging
from elice_library.database.config import db
from marshmallow import ValidationError
from typing import List
from elice_library.database.models.book import Book
from elice_library.database.models.user import User
from elice_library.database.models.book_rental import BookRental
from elice_library.utils.error_messages import BOOK_ALL_RENTED, BOOK_ALREADY_RENTED


class BookRentalService():
    @staticmethod
    def create(user, book) -> BookRental:        
        if not book.can_rent:
            raise ValidationError(BOOK_ALL_RENTED)

        rental = BookRentalService.find_last_by_ids(user.id, book.id)
        if rental and not rental.is_finished:
            raise ValidationError(BOOK_ALREADY_RENTED)
        
        book.rent()
        rental = BookRental(user=user, book=book)

        db.session.add(rental)
        db.session.commit()
        return rental

    @staticmethod
    def find_last_by_ids(user_id, book_id) -> BookRental:
        filtered = BookRental.query.filter_by(user_id=user_id, book_id=book_id).all()
        return filtered[-1] if filtered else None

    @staticmethod
    def find_all_by_user_id(user_id) -> List[BookRental]:
        return BookRental.query.filter_by(user_id=user_id).all()

    @staticmethod
    def find_not_finished_by_user_id(user_id) -> List[BookRental]:
        all_rentals = BookRentalService.find_all_by_user_id(user_id)
        return [rental for rental in all_rentals if not rental.is_finished]

    @staticmethod
    def finish_rental(user_id, book_id) -> BookRental:
        book = Book.find_by_id(book_id)
        book.get_returned()

        existed = BookRentalService.find_last_by_ids(user_id, book_id)
        existed.finish()
        return existed
