
from elice_library.database.config import db
from datetime import datetime
from pytz import timezone


class BookRental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id', ondelete='CASCADE'))
    book = db.relationship('Book', backref=db.backref('rental_set'))
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref("rental_set"))
    rented_at = db.Column(db.DateTime, nullable=False,
                          default=datetime.now(timezone('Asia/Seoul')))
    returned_at = db.Column(db.DateTime, nullable=True)
