import logging
from elice_library.database.config import db, ma


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_name = db.Column(db.String(128), nullable=False)
    publisher = db.Column(db.String(128), nullable=False)
    author = db.Column(db.String(128), nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)
    pages = db.Column(db.Integer, nullable=False)
    isbn = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.Text, nullable=False)
    image_path = db.Column(db.Text)
    stock_num = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Integer, nullable=False, default=0)

    @property
    def has_stock(self):
        return self.stock_num >= 1

    def add_stock(self):
        self.stock_num += 1
        db.session.commit()
        return self.stock_num

    def reduce_stock(self):
        self.stock_num -= 1
        db.session.commit()
        return self.stock_num

    def add_rental_info(self, rental):
        self.rental_list.append(rental)
        return self.rental_list

    def add_comment(self, comment):
        self.comments.append(comment)
        return self.comments

    def update_rating(self):
        self.rating = round(
            sum([comment.rating for comment in self.comments])/len(self.comments))
        db.session.commit()
        return self.rating

    def __repr__(self):
        return "<Book(id='%s', name='%s', publisher='%s', author='%s', published_at='%s')>" % (
            self.id, self.book_name, self.publisher, self.author, self.published_at)

    @staticmethod
    def get_all():
        return Book.query.all()

    @staticmethod
    def find_by_id(id):
        return Book.query.filter_by(id=id).first()

    @staticmethod
    def sort_by_rentals_num():
        books = Book.get_all()
        sorted_books = [book for book in sorted(books, key=lambda x:len(x.comments), reverse=True)]
        return sorted_books

    @staticmethod
    def sort_by_published_date():
        books = Book.get_all()
        sorted_books = [book for book in sorted(books, key=lambda x:x.published_at, reverse=True)]
        return sorted_books

    @staticmethod
    def sort_by_comments_num():
        books = Book.get_all()
        sorted_books = [book for book in sorted(books, key=lambda x:len(x.comments), reverse=True)]
        return sorted_books

class BookSchema(ma.Schema):
    class Meta:
        fields = ("id", "book_name", "publisher", "author", "published_at",
                  "pages", "isbn", "description", "link", "image_path", "stock_num", "rating")
