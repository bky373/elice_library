from flask import Blueprint, render_template
from elice_library.models import Book, BookSchema

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('books/book_list.html')
