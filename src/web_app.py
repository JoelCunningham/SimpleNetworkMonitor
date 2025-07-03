import sys
import threading
import time

from flask import Flask, jsonify, render_template
from flask_socketio import SocketIO, emit  # type: ignore

from Constants import DEFAULT_CONFIG_PATH
from Services.ServiceContainer import ServiceContainer

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
container = ServiceContainer(DEFAULT_CONFIG_PATH)
scanning = False


@app.route('/')
def index():
    """Main dashboard page."""
    return render_template('index.html')


@app.route('/api/devices')
def get_devices():
    """Get all devices from database."""
    if not container:
        return jsonify({'error': 'Services not initialized'}), 500
    
    try:
        device_repo = container.device_repository()
        mac_devices = device_repo.get_all_devices() 
        
        device_list: list[dict[str, int | str | None]] = []
        for mac in mac_devices:
            device_data = {
                'id': mac.id,
                'mac_address': mac.address,
                'vendor': mac.vendor if hasattr(mac, 'vendor') else 'Unknown',
                'device_model': mac.device.model if mac.device and mac.device.model else 'Unknown',
                'category': mac.device.category.name if mac.device and mac.device.category else 'Unknown',
                'owner': mac.device.owner.name if mac.device and mac.device.owner else 'Unknown',
                'location': mac.device.location.name if mac.device and mac.device.location else 'Unknown',
                'last_seen': mac.last_seen.isoformat() if hasattr(mac, 'last_seen') and mac.last_seen else None
            }
            device_list.append(device_data)
        
        return jsonify(device_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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




def perform_network_scan():
    """Perform the actual network scan and emit results via websocket."""
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
            'message': f'Found {len(devices)} devices. Processing...', 
            'type': 'info'
        }) 
        
        from typing import Any, Dict, List
        processed_devices: List[Dict[str, Any]] = []
        
        for i, device in enumerate(devices):
            # Emit progress update
            progress = int((i / len(devices)) * 100)
            socketio.emit('scan_progress', {'progress': progress, 'current': i + 1, 'total': len(devices)})  # type: ignore
            
            from typing import Any, List
            device_data: dict[str, Any] = {
                'ip_address': device.ip_address,
                'mac_address': device.mac_address,
                'hostname': device.hostname,
                'mac_vendor': device.mac_vendor,
                'os_guess': device.os_guess,
                'ping_time_ms': device.ping_time_ms,
                'arp_time_ms': device.arp_time_ms,
                'ports': [],        
                'services': [],      
                'discoveries': [],  
            }
            
            # Save to database if MAC address is available
            if device.mac_address:
                try:
                    mac_record = device_repo.save_device(device)
                    scan_data_repo.save_scan_results(mac_record, device)
                    device_data['saved'] = True
                except Exception as e:
                    device_data['saved'] = False
                    device_data['save_error'] = str(e)
            
            # Get scan summary
            ports, services, discoveries = scanner.get_scan_summary(device)
            device_data['ports'] = ports
            device_data['services'] = services
            device_data['discoveries'] = discoveries
            
            processed_devices.append(device_data)
            
            # Emit individual device result
            socketio.emit('device_found', device_data)  # type: ignore
            
            time.sleep(0.1)  # Small delay to prevent overwhelming the client
        
        socketio.emit('scan_complete', {  # type: ignore
            'message': f'Scan completed. {len(devices)} devices processed.',
            'devices': processed_devices,
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