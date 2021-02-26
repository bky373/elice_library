
from elice_library.database.config import db
from datetime import datetime
from pytz import timezone


class BookRental(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref("rental_set"))
    book = db.relationship('Book', backref=db.backref('rental_set'))
    rented_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone('Asia/Seoul')))
    returned_at = db.Column(db.DateTime, nullable=True)

    
    def __repr__(self):
        return "<BookRental(id='%s', user_id='%s', book_id='%s', rented_at='%s', returned_at='%s')>" % (
            self.id, self.user_id, self.book_id, self.rented_at, self.returned_at
        )
