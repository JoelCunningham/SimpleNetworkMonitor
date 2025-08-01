"""
API interface routes.

This blueprint handles all API endpoints for the application.
"""
import json
import os
from typing import Any

from flask import Blueprint, current_app, jsonify, request

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
        
        return jsonify(devices_raw)
    except Exception as e:
        return jsonify({'error': f'Failed to get devices: {str(e)}'}), 500

@api_bp.route('/devices/save', methods=['POST'])
def save_device():
    """Save a device to the database."""
    try:
        data = json.loads(request.data)
        
        model = data.get('model')
        category_id = data.get('category_id')
        location_id = data.get('location_id')
        owner_id = data.get('owner_id')
        mac_ids = data.get('mac_ids')

        controller = container.device_controller()
        device = controller.add_device(model, category_id, location_id, owner_id, mac_ids)
        
        device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
        
        return device_raw, 201
    except Exception as e:
        return jsonify({'error': f'Failed to save device: {str(e)}'}), 500

@api_bp.route('/devices/<mac_address>', methods=['GET'])
def get_device(mac_address: str):
    """Get a device by its MAC address."""
    try:
        controller = container.device_controller()
        device = controller.get_device(mac_address)
        
        if device:
            device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
            return jsonify(device_raw)
        else:
            return jsonify({'error': 'Device not found'}), 404
    except Exception as e:
        return jsonify({'error': f'Failed to get device: {str(e)}'}), 500


@api_bp.route('/devices/options', methods=['GET'])
def get_device_options():
    """Get options for device categories, locations, and owners."""
    try:
        controller = container.device_controller()
        categories = controller.get_device_categories()
        locations = controller.get_device_locations()
        owners = controller.get_device_owners()

        options = {
            'categories': [{'id': c.id, 'name': c.name} for c in categories],
            'locations': [{'id': l.id, 'name': l.name} for l in locations],
            'owners': [{'id': o.id, 'name': o.name} for o in owners]
        }

        return jsonify(options)
    except Exception as e:
        return jsonify({'error': f'Failed to get device options: {str(e)}'}), 500

@api_bp.route('/owners/save', methods=['POST'])
def save_owner():
    """Save a new owner."""
    try:
        data = json.loads(request.data)
        name = data.get('name')
        
        controller = container.device_controller()
        owner = controller.add_owner(name)

        owner_raw = json.loads(json.dumps(owner, cls=ModelEncoder))
        
        return jsonify(owner_raw), 201
    except Exception as e:
        print(f"Error saving owner: {str(e)}")
        return jsonify({'error': f'Failed to save owner: {str(e)}'}), 500