"""
API interface routes.

This blueprint handles all API endpoints for the application.
"""
import json

from flask import Blueprint, jsonify

from app import container
from app.utilities.model_encoder import ModelEncoder

api_bp = Blueprint('category', __name__)

@api_bp.route('/', methods=['GET'])
def get_categories():
    """Get all device categories."""
    try:
        categories = container.category_service().get_categories()
        categories_raw = [json.loads(json.dumps(category, cls=ModelEncoder)) for category in categories]

        return jsonify(categories_raw), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get categories: {str(e)}'}), 500