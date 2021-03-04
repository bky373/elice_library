from typing import List
from elice_library.database.config import db
from elice_library.domain.models.book import Book


class BookService:
    def find_all(self) -> List[Book]:
        return Book.query.all()

    def find_by_id(self, book_id) -> Book:
        return Book.query.filter_by(id=book_id).first()

    def paginate(self, page, per_page):
        return Book.query.paginate(page, per_page)
    
    def sort_by_rentals_num(self) -> List[Book]:
        books = self.find_all()
        return sorted(books, key=lambda x:len(x.rental_list), reverse=True)

    def sort_by_published_date(self) -> List[Book]:
        books = self.find_all()
        return sorted(books, key=lambda x:x.published_at, reverse=True)

    def sort_by_comments_num(self) -> List[Book]:
        books = self.find_all()
        return sorted(books, key=lambda x:len(x.comments), reverse=True)