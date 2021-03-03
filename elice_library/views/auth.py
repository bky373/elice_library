from flask import Blueprint, request, abort, jsonify, g, session, redirect, render_template, url_for
from marshmallow import ValidationError
from elice_library.domain.schemas.user_schema import UserCreateSchema, UserLoginSchema
from elice_library.services.user_service import UserService

auth_bp = Blueprint('auth', __name__)

user_create_schema = UserCreateSchema()
user_login_schema = UserLoginSchema()
user_service = UserService()

@auth_bp.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        try:
            json_data = request.get_json()
            data = user_create_schema.load(json_data)

            username, email, password, re_password = data[
                'username'], data['email'], data['password'], data['repassword']

            user = user_service.register_user(
                username=username, 
                email=email, 
                password=password, 
                re_password=re_password
            )

        except ValidationError as e:
            return {'message' : e.messages}, 400

        return {'username': user.username}, 201
    return render_template('auth/signup.html')


@auth_bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        try:
            json_data = request.get_json()
            data = user_login_schema.load(json_data)

            email, password = data['email'], data['password']
            
            user = user_service.login(email, password)

            session.pop('user_id', None)
            session['user_id'] = user.id
            
        except ValidationError as e:
            return {'message' : e.messages}, 400

        return {'username': user.username}, 201
    return render_template('auth/login.html')


@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    g.user = user_service.find_by_id(user_id) if user_id else None


@auth_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('main.index'))
