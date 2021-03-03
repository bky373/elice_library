from elice_library.database.config import db
from typing import List
from elice_library.database.models.book import Book


class BookService():
    @staticmethod
    def find_all() -> List[Book]:
        return Book.query.all()

    @staticmethod
    def find_by_id(id) -> Book:
        return Book.query.filter_by(id=id).first()

    @staticmethod
    def sort_by_rentals_num() -> List[Book]:
        books = BookService.find_all()
        return sorted(books, key=lambda x:len(x.rental_list), reverse=True)

    @staticmethod
    def sort_by_published_date() -> List[Book]:
        books = BookService.find_all()
        return sorted(books, key=lambda x:x.published_at, reverse=True)

    @staticmethod
    def sort_by_comments_num() -> List[Book]:
        books = BookService.find_all()
        return sorted(books, key=lambda x:len(x.comments), reverse=True)

    @staticmethod
    def paginate(page, per_page):
        return Book.query.paginate(page, per_page)
        