from flask import Blueprint, redirect, url_for
from elice_library.models import Book, BookSchema

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return redirect(url_for('books.book_list'))
