from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_pymongo import PyMongo

from config import config

mongo = PyMongo()
login_manager = LoginManager()
mail = Mail()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # init app
    mongo.init_app(app)
    mail.init_app(app)

    # init login manager
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.session_protection = 'strong'

    # registration blueprints
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .errors import error as error_blueprint
    app.register_blueprint(error_blueprint)

    return app
