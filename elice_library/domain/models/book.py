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
    def can_rent(self):
        return self.stock_num >= 1

    def rent(self):
        self.stock_num -= 1
        return self

    def get_returned(self):
        self.stock_num += 1
        return self

    def update_rating(self):
        self.rating = round(sum([comment.rating for comment in self.comments])/len(self.comments))
        return self.rating

    def __repr__(self):
        return "<Book(id='%s', name='%s', publisher='%s', author='%s', published_at='%s')>" % (
            self.id, self.book_name, self.publisher, self.author, self.published_at)
