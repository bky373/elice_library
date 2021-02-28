import logging
from flask import Blueprint, request, abort, jsonify, g, session, redirect, render_template, url_for
from elice_library import db
from elice_library.database.models.user import User, UserCreateSchema, UserLoginSchema
from marshmallow import ValidationError
from elice_library.utils.errors import REQUIRED_INPUT_DATA, PASSWORDS_DO_NOT_MATCH, ALREADY_EXIST_ACCOUNT

auth_bp = Blueprint('auth', __name__)
user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()


@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data: return {"message": "No input data provided"}, 400

        try:
            data = user_create_schema.load(json_data)
            username, email, password, re_password = data[
                'username'], data['email'], data['password'], data['repassword']

        except ValidationError as e:
            logging.warning(e.messages)
            return e.messages, 422

        if not re_password:
            return jsonify({'message' : REQUIRED_INPUT_DATA}), 400 
        if password != re_password:
            return jsonify({'message' : PASSWORDS_DO_NOT_MATCH}), 400 

        user = User.create(username=username, email=email, password=password)
        return {'username': user.username}, 201
    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}
        try:
            data = user_login_schema.load(json_data)
            email, password = data['email'], data['password']

        except ValidationError as err:
            logging.warning(err.messages)
            return err.messages, 422

        user = User.find_by_email(email)
        if not user:
            return {'message': 'This email does not exist'}, 400
        elif not user.check_password(password):
            return {'message': 'Passwords do not match'}, 400

        session.pop('user_id', None)
        session['user_id'] = user.id
        return {'username': user.username}, 201
    return render_template('auth/login.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = User.find_by_id(user_id) if user_id else None


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))
