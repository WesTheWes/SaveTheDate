from flask import Flask, render_template
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.mail import Mail
from config import config

login_manager = LoginManager()
db = SQLAlchemy()
mail = Mail()

def create_app(config_name):

    app = Flask(__name__)

    # Initializing config keys
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # Initializing all dependencies
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    # Attach blueprints
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from rsvp import rsvp as rsvp_blueprint
    app.register_blueprint(rsvp_blueprint, url_prefix='/rsvp')

    return app