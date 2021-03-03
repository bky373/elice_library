from flask import Blueprint, render_template, request
from elice_library.services.book_service import BookService
from elice_library import db

books_bp = Blueprint('books', __name__, url_prefix='/books')

ROWS_PER_PAGE = 8


@books_bp.route('/')
def book_list():
    page = request.args.get('page', type=int, default=1)
    books = BookService.paginate(page, per_page=ROWS_PER_PAGE)
    return render_template('books/book_list.html', books=books)


@books_bp.route('/<int:book_id>')
def book_detail(book_id):
    return render_template('books/book_detail.html', book=BookService.find_by_id(book_id))


@books_bp.route('/new-arrivals')
def new_arrivals():
    return render_template('books/new_arrivals.html', books=BookService.sort_by_published_date())
