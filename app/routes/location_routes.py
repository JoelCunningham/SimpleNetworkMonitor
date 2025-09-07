"""
API interface routes.

This blueprint handles all API endpoints for the application.
"""
import json

from flask import Blueprint, jsonify

from app import container
from app.utilities.model_encoder import ModelEncoder

api_bp = Blueprint('location', __name__)


@api_bp.route('/', methods=['GET'])
def get_locations():
    """Get all device locations."""
    try:
        locations = container.location_service().get_locations()
        locations_raw = [json.loads(json.dumps(location, cls=ModelEncoder)) for location in locations]

        return jsonify(locations_raw)
    except Exception as e:
        return jsonify({'error': f'Failed to get locations: {str(e)}'}), 500
    
    