from flask import Blueprint, render_template, request
from elice_library.models import Book, BookSchema
from elice_library import db

books_bp = Blueprint('books', __name__, url_prefix='/books')
book_schema = BookSchema()

ROWS_PER_PAGE = 8


@books_bp.route('/')
def get_books():
    page = request.args.get('page', type=int, default=1)
    books = Book.query.paginate(page, per_page=ROWS_PER_PAGE)
    return render_template('books/book_list.html', books=books)


@books_bp.route('/<int:book_id>')
def get_book(book_id):
    book = Book.query.filter_by(id=book_id).first()
    return render_template('books/book_detail.html', book=book_schema.dump(book))
