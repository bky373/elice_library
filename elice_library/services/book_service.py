from typing import List
from elice_library.database.config import db
from elice_library.domain.models.book import Book


ADD_BOOKMARK = "을(를) 찜했습니다."
CANCEL_BOOKMARK = "찜하기를 취소했습니다."

ADD_RECOMMENDATION = "추천하였습니다."
CANCEL_RECOMMENDATION = "추천을 취소하였습니다."


def get_all_books() -> List[Book]:
    return Book.query.all()


def get_book_by_id(book_id) -> Book:
    return Book.query.filter_by(id=book_id).first()


def paginate_books(page, per_page):
    return Book.query.paginate(page, per_page)


def mark_book_by_user(user, book_id):
    book = get_book_by_id(book_id)
    if user in book.markers:
        book.markers.remove(user)
        db.session.commit()
        return {"message": CANCEL_BOOKMARK, "result": "cancel"}

    book.markers.append(user)
    db.session.commit()
    return {"message": f'"{book.book_name}"{ADD_BOOKMARK}', "result": "add"}


def recommend_book_by_user(user, book_id):
    book = get_book_by_id(book_id)
    if user in book.voters:
        book.voters.remove(user)
        db.session.commit()
        return {"message": CANCEL_RECOMMENDATION, "result": "cancel"}

    book.voters.append(user)
    db.session.commit()
    return {"message": ADD_RECOMMENDATION, "result": "add"}


def sort_books_by_rentals_num() -> List[Book]:
    books = get_all_books()
    return sorted(books, key=lambda x: len(x.rental_list), reverse=True)


def sort_books_by_rating() -> List[Book]:
    books = get_all_books()
    return sorted(books, key=lambda x: x.rating, reverse=True)


def sort_books_by_published_date() -> List[Book]:
    books = get_all_books()
    return sorted(books, key=lambda x: x.published_at, reverse=True)


def sort_books_by_comments_num() -> List[Book]:
    books = get_all_books()
    return sorted(books, key=lambda x: len(x.comments), reverse=True)
