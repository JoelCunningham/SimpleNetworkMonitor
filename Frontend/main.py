import json
import os
import sys
import threading
from typing import Any, List

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit  # type: ignore

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Backend.Constants import DEFAULT_CONFIG_PATH
from Backend.Services.ServiceContainer import ServiceContainer
from Backend.Utilities.ModelEncoder import ModelEncoder

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
container = ServiceContainer(DEFAULT_CONFIG_PATH)
scanning = False


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/api/scan/start', methods=['POST'])
def start_scan():
    """Start a network scan."""
    global scanning
    
    if scanning:
        return jsonify({'error': 'Scan already in progress'}), 400
    
    scanning = True
    
    # Start scan in background thread
    thread = threading.Thread(target=_perform_network_scan)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Scan started'})


@app.route('/api/scan/status')
def get_scan_status():
    """Get current scan status."""
    return jsonify({'scanning': scanning})


@app.route('/api/scan/latest')
def get_latest_scan():
    """Get the date of the lastest scan."""
    repository = container.data_repository()
    latest_scan = repository.get_latest_scan_date()
    
    if latest_scan:
        return jsonify({'latest_scan': latest_scan.isoformat()})
    else:
        return jsonify({'latest_scan': None})


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


@app.route('/api/devices')
def get_devices():
    """Get all devices from database."""
    try:
        device_repo = container.data_repository()
        devices = device_repo.get_all_devices()
        devices_raw = json.loads(json.dumps(devices, cls=ModelEncoder))
        return jsonify({'devices': devices_raw})
    except Exception as e:
        print(f"Failed to load devices: {str(e)}")
        return jsonify({'error': f'Failed to load devices: {str(e)}'}), 500


def _perform_network_scan():
    """Perform the actual network scan and save results to database."""
    global scanning
    
    try:
        socketio.emit('scan_update', {'message': 'Starting network scan...', 'type': 'info'}) # type: ignore
        
        scanner = container.network_scanner()
        repository = container.data_repository()
        
        socketio.emit('scan_update', {'message': 'Scanning network...', 'type': 'info'})  # type: ignore
        
        scanned_devices = scanner.scan_network()
        
        if not scanned_devices:
            socketio.emit('scan_update', {'message': 'No devices found on the network.', 'type': 'warning'})  # type: ignore
            return
        
        socketio.emit('scan_update', {  # type: ignore
            'message': f'Found {len(scanned_devices)} devices. Saving to database...', 
            'type': 'info'
        }) 
        
        saved_count = 0
        
        for i, device in enumerate(scanned_devices):
            progress = int((i / len(scanned_devices)) * 100)
            socketio.emit('scan_progress', {'progress': progress, 'current': i + 1, 'total': len(scanned_devices)})  # type: ignore
            
            if device.mac_address:
                try:
                    repository.save_scan_result(device)
                    saved_count += 1
                except Exception as e:
                    socketio.emit('scan_update', {  # type: ignore
                        'message': f'Failed to save device {device.ip_address}: {str(e)}', 
                        'type': 'warning'
                    })
              
        all_devices = repository.get_known_unknown_devices(scanned_devices)  
        all_devices_raw: List[Any] = []
        for device in all_devices:
            device_raw = json.loads(json.dumps(device, cls=ModelEncoder))
            all_devices_raw.append(device_raw)

        socketio.emit('scan_complete', {  # type: ignore
            'message': f'Scan completed. {saved_count} of {len(scanned_devices)} devices saved to database.',
            'devices': all_devices_raw,
            'type': 'success'
        })
                
    except Exception as e:
        socketio.emit('scan_error', {'message': f'Scan error: {str(e)}', 'type': 'error'})  # type: ignore
    
    scanning = False


@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    print('Client connected')
    emit('connected', {'message': 'Connected to Network Monitor'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')


if __name__ == '__main__':
    print("=" * 60)
    print("Simple Network Monitor - Web Interface")
    print("=" * 60)
    print() 
    print("✓ Starting web server...")
    print()
    print("🌐 Open your browser to: http://localhost:5000")
    print("🔧 Press Ctrl+C to stop the server")
    print()
    
    try:
        socketio.run(app, host='0.0.0.0', port=5000, debug=True)  # type: ignore
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)