"""
SimpleNetworkMonitor Flask Application

A network monitoring tool that discovers and tracks devices on your network.
"""
import os
import threading
import time

from flask import Flask
from flask_cors import CORS

from app.container import Container
from app.database import Database
from app.config import Config

container = Container()
database = Database()
config = Config() 

def create_app():
    """Application factory pattern for creating Flask app instances."""
    app = Flask(__name__)
    
    # Update Flask configuration from the config
    app.config.update({  # type: ignore[misc]
        'DEBUG': config.debug,
        'TESTING': config.testing,
        'SQLALCHEMY_DATABASE_URI': config.database_url,
        'SQLALCHEMY_TRACK_MODIFICATIONS': config.sqlalchemy_track_modifications,
        'SQLALCHEMY_ECHO': config.sqlalchemy_echo,
    })
    
    # Initialize extensions
    with app.app_context():
        database.init(app)
        container.init(app)
    
    # Start background scanning
    if os.environ.get('WERKZEUG_RUN_MAIN') == 'true' or not app.debug:
       threading.Thread(target=_start_scanning, daemon=True).start()
        
    # Register blueprints
    from app.routes.device_routes import api_bp as device_bp
    from app.routes.owner_routes import api_bp as owner_bp
    from app.routes.category_routes import api_bp as category_bp
    from app.routes.location_routes import api_bp as location_bp
    app.register_blueprint(device_bp, url_prefix='/api/devices')
    app.register_blueprint(owner_bp, url_prefix='/api/owners')
    app.register_blueprint(category_bp, url_prefix='/api/categories')
    app.register_blueprint(location_bp, url_prefix='/api/locations')

    # Enable CORS for frontend development
    CORS(app, origins=["http://localhost:4200"])

    return app

def _start_scanning(delay: int = 5):
    time.sleep(delay)
    container.scanning_service().start_continuous_scan()
