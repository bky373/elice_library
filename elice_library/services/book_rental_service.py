import logging
from elice_library.database.config import db
from marshmallow import ValidationError
from typing import List
from elice_library.database.models.book_rental import BookRental
from elice_library.services.book_service import BookService
from elice_library.utils.error_messages import BOOK_ALL_RENTED, BOOK_ALREADY_RENTED


class BookRentalService:
    book_service = BookService()

    def find_all_by_user_id(self, user_id) -> List[BookRental]:
        return BookRental.query.filter_by(user_id=user_id).all()

    def find_not_finished_by_user_id(self, user_id) -> List[BookRental]:
        user_all_rentals = self.find_all_by_user_id(user_id)
        return [rental for rental in user_all_rentals if not rental.is_finished]

    def find_last_by_ids(self, user_id, book_id) -> BookRental:
        filtered = BookRental.query.filter_by(user_id=user_id, book_id=book_id).all()
        return filtered[-1] if filtered else None

    def start_rent(self, user, book) -> BookRental:
        if not book.can_rent:
            raise ValidationError(BOOK_ALL_RENTED)
        
        rental = self.find_last_by_ids(user.id, book.id)
        if rental is not None and not rental.is_finished:
            raise ValidationError(BOOK_ALREADY_RENTED)

        rental = BookRental.create(user=user, book=book)
        book.rent()

        self.save_to_db(rental)
        return rental
    
    def finish_rent(self, user_id, book_id) -> BookRental:
        book = self.book_service.find_by_id(book_id)
        book.get_returned()

        selected = self.find_last_by_ids(user_id, book_id)
        selected.finish_rental()
        self.save_to_db(selected)
        return selected

    def save_to_db(self, rental) -> None:
        db.session.add(rental)
        db.session.commit()
