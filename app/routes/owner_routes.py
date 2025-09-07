"""
API interface routes.

This blueprint handles all API endpoints for the application.
"""
import json

from flask import Blueprint, jsonify, request

from app import container
from app.utilities.model_encoder import ModelEncoder

api_bp = Blueprint('owner', __name__)

@api_bp.route('/', methods=['GET']) 
def get_owners():
    """Get all device owners."""
    try:
        owners = container.owner_service().get_owners()      
        owners_raw = [json.loads(json.dumps(owner, cls=ModelEncoder)) for owner in owners]
        
        return jsonify(owners_raw), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get owners: {str(e)}'}), 500   

@api_bp.route('/', methods=['POST'])
def save_owner():
    """Save a new owner."""
    try:
        data = json.loads(request.data)
        name = data.get('name')
        device_ids = data.get('device_ids', [])

        owner = container.owner_service().add_owner(name, device_ids)
        owner_raw = json.loads(json.dumps(owner, cls=ModelEncoder))

        return jsonify(owner_raw), 201
    except Exception as e:
        print(f"Error saving owner: {str(e)}")
        return jsonify({'error': f'Failed to save owner: {str(e)}'}), 500

@api_bp.route('/<int:owner_id>', methods=['PUT'])
def update_owner(owner_id: int):
    """Update an existing owner."""
    try:
        data = json.loads(request.data)
        name = data.get('name')
        device_ids = data.get('device_ids', [])

        owner = container.owner_service().update_owner(owner_id, name, device_ids)

        owner_raw = json.loads(json.dumps(owner, cls=ModelEncoder))

        return jsonify(owner_raw), 200
    except Exception as e:
        print(f"Error updating owner: {str(e)}")
        return jsonify({'error': f'Failed to update owner: {str(e)}'}), 500
    
@api_bp.route('/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id: int):
    """Delete an owner by their ID."""
    try:
        container.owner_service().delete_owner(owner_id)
        return jsonify({'message': 'Owner deleted successfully.'}), 204
    except Exception as e:
        return jsonify({'error': f'Failed to delete owner: {str(e)}'}), 500