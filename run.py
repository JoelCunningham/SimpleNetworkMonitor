"""
Application entry point.

This is the main entry point for running the Flask application.
"""
import os
from app import create_app

PORT = 5000

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("Simple Network Monitor")
    print("=" * 60)
    print(f"⚙️ Configuration: {os.environ.get('FLASK_CONFIG', 'Default')}")
    print(f"🌐 Open your browser to: http://localhost:{PORT}")
    print(f"🔧 Press Ctrl+C to stop the server")
    print()
    
    app.run(host='0.0.0.0', port=PORT, debug=True)
