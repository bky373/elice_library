from flask import Blueprint
from elice_library.models import Book, BookSchema

books_bp = Blueprint('books', __name__)
book_schema = BookSchema(many=True)


@books_bp.route('/books')
def book_list():
    return {'books': book_schema.dump(Book.query.all())}
