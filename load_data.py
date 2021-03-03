import csv
import random
from datetime import date, datetime

from elice_library import create_app
from elice_library.database.config import db
from elice_library.domain.models.book import Book


app = create_app()
with app.app_context():
    with open('library_data.csv', 'r', encoding='UTF8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            published_at = datetime.strptime(
                row['publication_date'], '%Y-%m-%d'
            ).date()
            image_path = f"/static/images/{row['id']}"
            try:
                open(f'elice_library/{image_path}.png')
                image_path += '.png'
            except:
                image_path += '.jpg'

            book = Book(
                book_name=row['book_name'],
                publisher=row['publisher'],
                author=row['author'],
                published_at=published_at,
                pages=int(row['pages']),
                isbn=row['isbn'],
                description=row['description'],
                link=row['link'],
                image_path=image_path,
                stock_num=random.randrange(1,6),
                rating=random.randrange(1,6)
            )
            db.session.add(book)
        db.session.commit()
