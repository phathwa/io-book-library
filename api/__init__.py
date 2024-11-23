import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="urllib3")

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from swagger import init_swagger


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    swagger = init_swagger(app)

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    return app
