from flask import Blueprint, request, abort, jsonify, g, session
from elice_library import db
from elice_library.models import User
import json


auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        data = request.get_json()
        _username = data['username']
        _email = data['email']
        _password = data['password']

        if not _username or not _email or not _password:
            abort(400, message='입력값이 비어 있을 수 없습니다.')
        if User.query.filter_by(email=_email).first():
            abort(400, message='이미 등록된 이메일입니다.')
        print(_password)
        user = User(username=_username, email=_email)
        user.set_password(_password)
        db.session.add(user)
        db.session.commit()
        return jsonify(result=user.serialized), 201
    return jsonify(message="Signup Get Method Called")


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.get_json()
        _email = data['email']
        _password = data['password']

        if not _email or not _password:
            abort(400, message='입력값이 비어 있을 수 없습니다.')

        user = User.query.filter_by(email=_email).first()
        if not user:
            abort(400, message="등록되지 않은 계정입니다.")
        elif not user.check_password(_password):
            abort(400, message="비밀번호가 올바르지 않습니다")

        session.pop('user_id', None)
        session['user_id'] = user.id
        return jsonify(result=user.serialized)
    return jsonify(message='Login Get Method Called')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None if not user_id else User.query.filter_by(id=user_id).first()


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return jsonify(message='Logout Success')
