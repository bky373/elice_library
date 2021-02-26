import logging
from flask import Blueprint, request, abort, jsonify, g, session, redirect, render_template, url_for
from elice_library import db
from elice_library.database.models.user import User, UserCreateSchema, UserLoginSchema
from marshmallow import ValidationError

auth_bp = Blueprint('auth', __name__)
user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()


@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        try:
            data = user_create_schema.load(json_data)            
            username = data['username']
            email = data['email']
            password = data['password']
            re_password = data['repassword']

        except ValidationError as err:
            logging.warning(err.messages)
            return err.messages, 422

        if password != re_password:
            return {'message': 'Passwords do not match'}, 400

        user = User.create(username=username, email=email, password=password)
        # 이미 등록된 유저가 있을 때
        if not user:
            return {'message': 'This email is already registered'}, 400
        return {'user': user_create_schema.dump(user)}, 201
    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}
        try:
            data = user_login_schema.load(json_data)
            email = data['email']
            password = data['password']
            
        except ValidationError as err:
            logging.warning(err.messages)
            return err.messages, 422

        user = User.find_by_email(email=email)
        if not user:
            return {'message': 'This email does not exist'}, 400
        elif not user.check_password(password):
            return {'message': 'Passwords do not match'}, 400

        session.pop('user_id', None)
        session['user_id'] = user.id

        return {'user': user_login_schema.dump(user)}, 201
    return render_template('auth/login.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.find_by_id(user_id) if user_id else None 


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))
