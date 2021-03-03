from datetime import datetime
from pytz import timezone
from elice_library.database.config import db


class BookRental(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref("rental_list"))
    book = db.relationship('Book', backref=db.backref('rental_list'))
    rented_at = db.Column(db.DateTime, nullable=False)
    returned_at = db.Column(db.DateTime, nullable=True)

    def __init__(self, user, book):
        self.user = user
        self.book = book
        self.rented_at = datetime.now(timezone('Asia/Seoul'))

    @property
    def is_finished(self):
        return self.returned_at is not None

    def finish_rental(self):
        self.returned_at = datetime.now(timezone('Asia/Seoul'))
        return self.returned_at

    def __repr__(self):
        return "<BookRental(id='%s', user_id='%s', book_id='%s', rented_at='%s', returned_at='%s')>" % (
            self.id, self.user_id, self.book_id, self.rented_at, self.returned_at)

    @staticmethod
    def create(user, book):
        return BookRental(user=user, book=book)