from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from dotenv import load_dotenv
import os

load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
limiter = Limiter(key_func=get_remote_address)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Session security
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['PERMANENT_SESSION_LIFETIME'] = 1800

    # Security headers
    csp = {
        'default-src': "'self'",
        'style-src': ["'self'", 'cdn.jsdelivr.net', "'unsafe-inline'"],
        'script-src': ["'self'", 'cdn.jsdelivr.net'],
        'font-src': ["'self'", 'cdn.jsdelivr.net'],
        'img-src': ["'self'", 'data:'],
    }
    Talisman(app,
        force_https=False,
        content_security_policy=csp
    )

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    limiter.init_app(app)

    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from app.routes.auth import auth
    from app.routes.patient import patient
    from app.routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(patient)
    app.register_blueprint(admin)

    with app.app_context():
        from app import models
        db.create_all()

    return app
