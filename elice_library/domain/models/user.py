from datetime import datetime
from pytz import timezone
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash
from elice_library.database.config import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(128), primary_key=True, unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    joined_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = generate_password_hash(password)
        self.joined_at = datetime.now(timezone("Asia/Seoul"))

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return (
            "<User(id='%s', name='%s', email='%s', password='%s', joined_at='%s')>"
            % (self.id, self.username, self.email, self.password, self.joined_at)
        )

    @staticmethod
    def create(username, email, password):
        return User(username=username, email=email, password=password)
