from elice_library.database.config import db

book_voter = db.Table(
    "book_voter",
    db.Column(
        "user_id",
        db.Integer,
        db.ForeignKey("user.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    db.Column(
        "book_id",
        db.Integer,
        db.ForeignKey("book.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)
