"""
Web interface routes.

Simple routes that serve HTML templates for the SPA frontend.
"""
from flask import render_template, Blueprint

web_bp = Blueprint('web', __name__)


@web_bp.route('/')
@web_bp.route('/index')
def index():
    """Main dashboard page."""
    return render_template('index.html')
