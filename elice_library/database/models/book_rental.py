import logging
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

    
    def __init__(self, user, book):
        self.user = user
        self.book = book
    

    @staticmethod
    def create(user, book):
        try:            
            rental = BookRental(user=user, book=book)
            user.rental_set.append(rental)
            book.add_rental_info(rental)
            book.reduce_stock()

            db.session.add(rental)
            db.session.commit()
            return rental
        except Exception as e:
            logging.warning(e)
            return None


    @property
    def is_returned(self):
        return self.returned_at is not None

    
    def set_return_date(self):
        self.returned_at = datetime.utcnow()


    def __repr__(self):
        return "<BookRental(id='%s', user_id='%s', book_id='%s', rented_at='%s', returned_at='%s')>" % (
            self.id, self.user_id, self.book_id, self.rented_at, self.returned_at
        )
