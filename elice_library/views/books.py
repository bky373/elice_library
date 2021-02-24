from flask import Blueprint, render_template
from elice_library.models import Book, BookSchema
from elice_library import db
import csv

books_bp = Blueprint('books', __name__, url_prefix='/books')
book_schema = BookSchema()


@books_bp.route('/')
def get_books():
    return {'books': book_schema.dump(Book.query.all(), many=True)}


def init_books():
    with open('library_data.csv', newline='', encoding='UTF8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            if row[0] != ' ':
                book = Book(
                    book_name=row[1],
                    publisher=row[2],
                    author=row[3],
                    pulication_date=row[4],
                    pages=int(row[5]),
                    isbn=int(row[6]),
                    description=row[7],
                    link=row[8],
                    stock_num=1,
                    rating=3
                )
                db.session.add(book)
                db.session.commit()
