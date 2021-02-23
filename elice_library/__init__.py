from flask import Flask

def create_app():
    app = Flask(__name__)

    from elice_library.views.main import main_bp
    app.register_blueprint(main_bp)    

    return app
