import threading
from datetime import datetime, timedelta
from flask import Flask

from app import config
from app.models.device import Device
from app.objects.scan_options import ScanOptions
from app.services.device_service import DeviceService
from app.services.scan_service import ScanService

SCAN_CHECK_INTERVAL = 60 

class ScanController:
    """Scan controller that manages scanning operations."""

    def __init__(self, 
                 scan_service: ScanService,
                 device_service: DeviceService,
                 app: Flask) -> None:
        self.scan_service = scan_service
        self.device_service = device_service
        self.app = app
        
        self.scanning_thread: threading.Thread | None = None
        self.stop_event = threading.Event()
        self.is_scanning = False
        
        self.last_scan_time: datetime | None = None
        self.scan_error: str | None = None
        self.last_scan_results = []
        
        self.basic_scan_interval = config.background_scan_interval_s
        self.full_scan_interval = config.background_full_scan_interval_s
        
    def start_continuous_scan(self):
        """Start the background scanning service."""
        self.stop_event.clear()
        self.scanning_thread = threading.Thread(target=self._scan_loop_with_context, daemon=True)
        self.scanning_thread.start()
        
    def stop_continuous_scan(self):
        """Stop the background scanning service."""
        self.stop_event.set()
        if self.scanning_thread:
            self.scanning_thread.join(timeout=5)    
        
    def get_scan_status(self) -> dict[str, str | bool | None]:
        """Get current scanner status."""
        return {
            'is_scanning': self.is_scanning,
            'last_scan_time': self.last_scan_time.isoformat() if self.last_scan_time else None,
        }
        
    def get_latest_devices(self) -> list[Device]:
        """Get the latest scan results."""
        if not self.last_scan_results:
            return []
        return self.device_service.get_current_devices(self.last_scan_results)
        
    def _scan_loop_with_context(self):
        """Wrapper that ensures the scan loop runs with Flask app context."""
        with self.app.app_context():
            self._scan_loop()
        
    def _scan_loop(self):
        """Main scanning loop that runs in background thread."""        
        # Perform initial full scan
        self._perform_scan(full_scan=True)
        
        last_full_scan = datetime.now()
        last_basic_scan = datetime.now()
        
        while not self.stop_event.is_set():
            if self.stop_event.wait(timeout=SCAN_CHECK_INTERVAL):
                break
            
            if not self.is_scanning:                
                if last_full_scan >= datetime.now() - timedelta(seconds=self.full_scan_interval):
                    self._perform_scan(full_scan=True)
                    last_full_scan = datetime.now()
                    
                elif last_basic_scan >= datetime.now() - timedelta(seconds=self.basic_scan_interval):
                    self._perform_scan(full_scan=False)
                    last_basic_scan = datetime.now()
            
    def _perform_scan(self, full_scan: bool = False):
        """Perform the actual scan logic."""
        self.is_scanning = True
        
        try:
            if full_scan:
                scan_options = ScanOptions.full_scan()
                save_func = self.scan_service.save_full_scan
            else:
                scan_options = ScanOptions.mac_only()
                save_func = self.scan_service.save_mac_scan                
            
            scanned_devices = self.scan_service.scan_network(scan_options)
            
            if scanned_devices:
                for device in scanned_devices:
                    if device.mac_address:
                        save_func(device)
                            
                self.last_scan_results = scanned_devices             
            else:
                self.last_scan_results = []
                
            self.last_scan_time = datetime.now()
            
        except Exception as e:
            print(f"Scan error during {"full" if full_scan else "basic"} scan: {e}")
        finally:
            self.is_scanning = False
