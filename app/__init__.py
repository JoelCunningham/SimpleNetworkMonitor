"""
SimpleNetworkMonitor Flask Application

A network monitoring tool that discovers and tracks devices on your network.
"""
import os
import threading
import time

from flask import Flask

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
    from app.routes.web import web_bp
    from app.routes.api import api_bp
    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app

def _start_scanning(delay: int = 5):
    time.sleep(delay)
    container.scan_controller().start_continuous_scan()
