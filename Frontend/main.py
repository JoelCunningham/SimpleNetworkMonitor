import json
import os
import sys
from typing import Any

from flask import Flask, jsonify, render_template

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Constants import DEFAULT_CONFIG_PATH
from Backend.Services.ServiceContainer import ServiceContainer
from Backend.Utilities.ModelEncoder import ModelEncoder

app = Flask(__name__)
container = ServiceContainer(DEFAULT_CONFIG_PATH)
scanning = False

@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')

@app.route('/api/devices')
def get_devices():
    """Get all known devices from the latest scan."""
    try:
        background_scanner = container.background_scanner()
        all_devices = background_scanner.get_latest_devices()
        all_devices_raw: list[Any] = []
        
        for device in all_devices:
            device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
            all_devices_raw.append(device_raw)
        
        return jsonify({'devices': all_devices_raw})
        
    except Exception as e:
        print(f'Error getting devices: {str(e)}')
        return jsonify({'error': f'Failed to get devices: {str(e)}'}), 500


@app.route('/api/scan/status')
def get_scan_status():
    """Get the current scanning status."""
    try:
        background_scanner = container.background_scanner()
        status = background_scanner.get_status()
        return jsonify(status)
    except Exception as e:
        print(f'Error getting scan status: {str(e)}')
        return jsonify({'error': f'Failed to get scan status: {str(e)}'}), 500


@app.route('/api/icons/devices')
def get_device_icons():
    """Get list of available device icons."""
    if app.static_folder is None:
        return jsonify({'icons': []})
    
    icons_dir: str = os.path.join(app.static_folder, 'icons', 'devices')
    try:
        if os.path.exists(icons_dir):
            svg_files = [f for f in os.listdir(icons_dir) if f.endswith('.svg')]
            return jsonify({'icons': svg_files})
        else:
            return jsonify({'icons': []})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("=" * 60)
    print("Simple Network Monitor - Web Interface")
    print("=" * 60)
    print() 
    print("🔄 Starting background scanner...")
    container.background_scanner().start(10)
    print("✅ Starting web server...")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    print()
    
    try:
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except KeyboardInterrupt:
        print("👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    finally:
        container.close()