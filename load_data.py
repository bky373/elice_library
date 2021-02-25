from elice_library.models import Book
from elice_library import db
import csv


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
