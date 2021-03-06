import logging
from elice_library.database.config import db
from marshmallow import ValidationError
from typing import List
from elice_library.domain.models.book_rental import BookRental
from elice_library.services.user_service import get_user_by_id
from elice_library.services.book_service import get_book_by_id
from elice_library.utils.errors import BooksAllRentedError, BookAlreadyRentedError


def get_all_rentals_by_user_id(user_id) -> List[BookRental]:
    return BookRental.query.filter_by(user_id=user_id).all()


def get_unfinished_rentals_by_user_id(user_id) -> List[BookRental]:
    user_all_rentals = get_all_rentals_by_user_id(user_id)
    return [rental for rental in user_all_rentals if not rental.is_finished]


def get_last_rental_by_ids(user_id, book_id) -> BookRental:
    filtered = BookRental.query.filter_by(user_id=user_id, book_id=book_id).all()
    return filtered[-1] if filtered else None


def start_rent(user_id, book_id) -> BookRental:
    user = get_user_by_id(user_id)
    book = get_book_by_id(book_id)

    if not book.can_rent:
        raise BooksAllRentedError()

    rental = get_last_rental_by_ids(user.id, book.id)
    if rental is not None and not rental.is_finished:
        raise BookAlreadyRentedError()

    rental = BookRental.create(user=user, book=book)
    book.rent()

    save_to_db(rental)
    return rental


def finish_rent(user_id, book_id) -> BookRental:
    book = get_book_by_id(book_id)
    book.get_returned()

    rental = get_last_rental_by_ids(user_id, book_id)
    rental.finish_rent()
    save_to_db(rental)
    return rental


def get_rentals_by_user_id(user_id) -> List[BookRental]:
    user = get_user_by_id(user_id)
    return user.rental_list


def save_to_db(rental) -> None:
    db.session.add(rental)
    db.session.commit()
