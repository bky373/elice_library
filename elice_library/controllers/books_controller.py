from flask import render_template, request, make_response
from flask_restx import Namespace
from elice_library.services.book_service import BookService
from elice_library.controllers.auth_controller import Resource


ROWS_PER_PAGE = 8
book_service = BookService()

api = Namespace('books', description='book related operations')

@api.route('/')
class BookList(Resource):
    def get(self):
        page = request.args.get('page', type=int, default=1)
        books = book_service.paginate(page, per_page=ROWS_PER_PAGE)
        return make_response(render_template('books/book_list.html', books=books)) 

@api.route('/<int:book_id>')
class Book(Resource):
    def get(self, book_id):
        return make_response(render_template('books/book_detail.html', book=book_service.find_by_id(book_id)))


@api.route('/new-arrivals')
class NewArrivals(Resource):
    def get(self):
        return make_response(render_template('books/new_arrivals.html', books=book_service.sort_by_published_date()))


@api.route('/rating-best')
class RatingBest(Resource):
    def get(self):
        return make_response(render_template('books/rating_best.html', books=book_service.sort_by_rating()))