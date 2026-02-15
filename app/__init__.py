from flask import Flask
from .extensions import db, login_manager
from config import Config

def create_app(config_class=Config):
    app = Flask(__name__)

    # pull all the settings from config.py
    app.config.from_object(config_class)
    
    db.init_app(app)
    login_manager.init_app(app)

    login_manager.login_view = 'auth.login'

    from .auth import auth_bp
    from .main import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app