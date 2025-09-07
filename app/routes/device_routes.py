"""
API interface routes.

This blueprint handles all API endpoints for the application.
"""
import json
from typing import Any

from flask import Blueprint, jsonify, request

from app import container
from app.utilities.model_encoder import ModelEncoder

api_bp = Blueprint('device', __name__)

@api_bp.route('/', methods=['GET'])
def get_devices():
    """Get all known devices from the latest scan."""
    try:
        devices = container.device_service().get_current_devices()
        devices_raw: list[Any] = []
        
        for device in devices:
            device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
            devices_raw.append(device_raw)
        
        return jsonify(devices_raw), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get devices: {str(e)}'}), 500

@api_bp.route('/', methods=['POST'])
def save_device():
    """Save a device to the database."""
    try:
        data = json.loads(request.data)
        
        name = data.get('name')
        model = data.get('model')
        category_id = data.get('category_id')
        location_id = data.get('location_id')
        owner_id = data.get('owner_id')
        mac_ids = data.get('mac_ids', [])

        device = container.device_service().add_device(name, model, category_id, location_id, owner_id, mac_ids)
        device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
        
        return device_raw, 201
    except Exception as e:
        return jsonify({'error': f'Failed to save device: {str(e)}'}), 500

@api_bp.route('/<int:device_id>', methods=['PUT'])
def update_device(device_id: int):
    """Update an existing device."""
    try:
        data = json.loads(request.data)
        
        name = data.get('name')
        model = data.get('model')
        category_id = data.get('category_id')
        location_id = data.get('location_id')
        owner_id = data.get('owner_id')
        mac_ids = data.get('mac_ids', [])

        device = container.device_service().update_device(device_id, name, model, category_id, location_id, owner_id, mac_ids)
        device_raw = json.loads(json.dumps(device, cls=ModelEncoder))

        return jsonify(device_raw), 200
    except Exception as e:
        return jsonify({'error': f'Failed to update device: {str(e)}'}), 500

@api_bp.route('/<mac_address>', methods=['GET'])
def get_device(mac_address: str):
    """Get a device by its MAC address."""
    try:
        device = container.device_service().get_device(mac_address)
        
        if device:
            device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
            return jsonify(device_raw), 200
        else:
            return jsonify({'error': 'Device not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get device: {str(e)}'}), 500


@api_bp.route('/options', methods=['GET'])
def get_device_options():
    """Get options for device categories, locations, and owners."""
    try:
        categories = container.category_service().get_categories()
        locations = container.location_service().get_locations()
        owners = container.owner_service().get_owners()

        options = {
            'categories': [{'id': c.id, 'name': c.name} for c in categories],
            'locations': [{'id': l.id, 'name': l.name} for l in locations],
            'owners': [{'id': o.id, 'name': o.name} for o in owners]
        }

        return jsonify(options), 200
    except Exception as e:
        return jsonify({'error': f'Failed to get device options: {str(e)}'}), 500
