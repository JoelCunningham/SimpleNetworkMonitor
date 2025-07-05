import json
import os
import sys
import threading
import time

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
    thread = threading.Thread(target=perform_network_scan)
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Scan started'})


@app.route('/api/scan/status')
def get_scan_status():
    """Get current scan status."""
    return jsonify({'scanning': scanning})


@app.route('/api/devices')
def get_devices():
    """Get all devices from database."""
    try:
        device_repo = container.device_repository()
        devices = device_repo.get_all_devices()
        devices_data = json.loads(json.dumps(devices, cls=ModelEncoder))
        return jsonify({'devices': devices_data})
    except Exception as e:
        print(f"Failed to load devices: {str(e)}")
        return jsonify({'error': f'Failed to load devices: {str(e)}'}), 500


def perform_network_scan():
    """Perform the actual network scan and save results to database."""
    global scanning
    
    try:
        socketio.emit('scan_update', {'message': 'Starting network scan...', 'type': 'info'}) # type: ignore
        
        scanner = container.network_scanner()
        device_repo = container.device_repository()
        scan_data_repo = container.scan_data_repository()
        
        socketio.emit('scan_update', {'message': 'Scanning network...', 'type': 'info'})  # type: ignore
        
        devices = scanner.scan_network()
        
        if not devices:
            socketio.emit('scan_update', {'message': 'No devices found on the network.', 'type': 'warning'})  # type: ignore
            return
        
        socketio.emit('scan_update', {  # type: ignore
            'message': f'Found {len(devices)} devices. Saving to database...', 
            'type': 'info'
        }) 
        
        saved_count = 0
        
        for i, device in enumerate(devices):
            # Emit progress update
            progress = int((i / len(devices)) * 100)
            socketio.emit('scan_progress', {'progress': progress, 'current': i + 1, 'total': len(devices)})  # type: ignore
            
            # Save to database if MAC address is available
            if device.mac_address:
                try:
                    mac_record = device_repo.save_device(device)
                    scan_data_repo.save_scan_results(mac_record, device)
                    saved_count += 1
                except Exception as e:
                    socketio.emit('scan_update', {  # type: ignore
                        'message': f'Failed to save device {device.ip_address}: {str(e)}', 
                        'type': 'warning'
                    })
            
            time.sleep(0.1)  # Small delay to prevent overwhelming the database
        
        socketio.emit('scan_complete', {  # type: ignore
            'message': f'Scan completed. {saved_count} of {len(devices)} devices saved to database.',
            'devices_found': len(devices),
            'devices_saved': saved_count,
            'type': 'success'
        })
        
    except Exception as e:
        socketio.emit('scan_error', {'message': f'Scan error: {str(e)}', 'type': 'error'})  # type: ignore
    
    finally:
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