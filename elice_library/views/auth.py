from flask import Blueprint, request, abort, jsonify, g, session, redirect, render_template, url_for
from elice_library import db
from elice_library.models import User, UserCreateSchema, UserLoginSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)
user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()


@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}
        try:
            data = user_create_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        _username = data['username']
        _email = data['email']
        _password = data['password']
        re_password = data['repassword']

        if _password != re_password:
            return {'message': 'Passwords do not match'}
        if User.query.filter_by(email=_email).first():
            return {'message': 'This email is already registered'}, 400

        user = User(username=_username, email=_email)
        user.set_password(_password)

        db.session.add(user)
        db.session.commit()
        result = user_create_schema.dump(user)
        return {'user': result}, 201
    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}
        try:
            data = user_login_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        _email = data['email']
        _password = data['password']

        user = User.query.filter_by(email=_email).first()
        if not user:
            abort(400, message="등록되지 않은 계정입니다.")
        elif not user.check_password(_password):
            abort(400, message="비밀번호가 올바르지 않습니다")

        session.pop('user_id', None)
        session['user_id'] = user.id

        result = user_login_schema.dump(user)
        return {'user': result}, 201
    return render_template('auth/login.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = None if not user_id else User.query.filter_by(id=user_id).first()


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))
