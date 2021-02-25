from flask import Blueprint, render_template, request
from elice_library.models import Book, BookSchema
from elice_library import db
import csv

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


def init_books():
    with open('library_data.csv', newline='', encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] != ' ':
                book = Book(
                    book_name=row[1],
                    publisher=row[2],
                    author=row[3],
                    publication_date=row[4],
                    pages=int(row[5]),
                    isbn=int(row[6]),
                    description=row[7],
                    link=row[8],
                    stock_num=1,
                    rating=3
                )
                db.session.add(book)
                db.session.commit()
