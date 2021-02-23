from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('base.html')
