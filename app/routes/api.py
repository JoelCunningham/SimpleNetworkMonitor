"""
API interface routes.

This blueprint handles all API endpoints for the application.
"""
import json
import os
from typing import Any

from flask import Blueprint, current_app, jsonify

from app import container
from app.utilities.model_encoder import ModelEncoder

api_bp = Blueprint('api', __name__)

@api_bp.route('/scan/status', methods=['GET'])
def get_scan_status():
    """Get the current scanning status."""
    try:
        controller = container.scan_controller()
        status = controller.get_scan_status()
        return jsonify(status)
    except Exception as e:
        return jsonify({'error': f'Failed to get scan status: {str(e)}'}), 500
    

@api_bp.route('/icons/devices', methods=['GET'])
def get_device_icons():
    """Get list of available device icons."""
    try:
        if current_app.static_folder is None:
            return jsonify({'icons': []})
        
        icons_dir = os.path.join(current_app.static_folder, 'icons', 'devices')
        if os.path.exists(icons_dir):
            svg_files = [f for f in os.listdir(icons_dir) if f.endswith('.svg')]
            return jsonify({'icons': svg_files})
        else:
            return jsonify({'icons': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@api_bp.route('/devices', methods=['GET'])
def get_devices():
    """Get all known devices from the latest scan."""
    try:
        controller = container.scan_controller()
        devices = controller.get_latest_devices()
        
        devices_raw: list[Any] = []
        for device in devices:
            device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
            devices_raw.append(device_raw)
        
        return jsonify({'devices': devices_raw})
    except Exception as e:
        return jsonify({'error': f'Failed to get devices: {str(e)}'}), 500
    
@api_bp.route('/locations', methods=['GET'])
def get_device_locations():
    """Get all locations for devices."""
    try:
        controller = container.device_controller()
        locations = controller.get_device_locations()
        
        locations_raw: list[Any] = []
        for location in locations:
            locations_raw.append({"id": location.id, "name": location.name})

        return jsonify({'items': locations_raw})
    except Exception as e:
        return jsonify({'error': f'Failed to get device locations: {str(e)}'}), 500
    
@api_bp.route('/categories', methods=['GET'])
def get_device_categories():
    """Get all categories for devices."""
    try:
        controller = container.device_controller()
        categories = controller.get_device_categories()

        categories_raw: list[Any] = []
        for category in categories:
            categories_raw.append({"id": category.id, "name": category.name})

        return jsonify({'items': categories_raw})
    except Exception as e:
        return jsonify({'error': f'Failed to get device categories: {str(e)}'}), 500
    
@api_bp.route('/owners', methods=['GET'])
def get_device_owners():
    """Get all owners for devices."""
    try:
        controller = container.device_controller()
        owners = controller.get_device_owners()

        owners_raw: list[Any] = []
        for owner in owners:
            owners_raw.append({"id": owner.id, "name": owner.name})

        return jsonify({'items': owners_raw})
    except Exception as e:
        return jsonify({'error': f'Failed to get device owners: {str(e)}'}), 500