from pytz import timezone
from datetime import datetime
from elice_library.database.config import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    user = db.relationship('User', backref=db.backref('comments'))
    book_id = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))
    book = db.relationship('Book', backref=db.backref('comments'))
    content = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __init__(self, user, book, content, rating):
        self.user = user
        self.book = book
        self.content = content
        self.rating = rating
        self.posted_at = datetime.now(timezone('Asia/Seoul'))

    def update(self, content):
        self.content = content
        return self

    def __repr__(self):
        return (
            "<Comment(id='%s', user_id='%s', book_id='%s', content='%s', posted_at='%s', rating='%s')>" 
            % (self.id, self.user_id, self.book_id, self.content, self.posted_at, self.rating)
        )

    @staticmethod
    def create(user, book, content, rating):
        return Comment(user=user, book=book, content=content, rating=rating)
