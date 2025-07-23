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