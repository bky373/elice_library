import logging
from elice_library.database.config import db
from datetime import datetime


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey(
        'user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('comment_set'))
    book_id = db.Column(db.Integer, db.ForeignKey(
        'book.id', ondelete='CASCADE'), nullable=False)
    book = db.relationship('Book', backref=db.backref('comment_set'))
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    rating = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, user, book, content, rating):
        self.user = user
        self.book = book
        self.content = content
        self.rating = rating

    @staticmethod
    def create(user, book, content, rating):
        try:
            comment = Comment(user=user, book=book, content=content, rating=rating)
            db.session.add(user)
            db.session.commit()
            return comment
        except Exception as e:
            logging.warning(e)
            return None

    def __repr__(self):
        return "<Comment(id='%s', user_id='%s', book_id='%s', content='%s', posted_at='%s')>" % (
            self.id, self.user_id, self.book_id, self.content, self.posted_at
        )