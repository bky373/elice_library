from flask import Blueprint

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/')
def index():
    return 'Welcome to Borahm Library :) !!!!'

