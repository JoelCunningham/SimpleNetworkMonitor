import threading
from datetime import datetime
from typing import List, Optional

from Backend.Entities.DeviceModel import Device
from Backend.Objects.ScanOptions import ScanOptions
from Backend.Services.AppConfiguration import AppConfig
from Backend.Services.DataPersistence import DataRepository, MacRepository
from Backend.Services.NetworkScanner import NetworkScanner


class BackgroundScanner:
    """Background scanning service that runs continuous network scans."""
    
    def __init__(self, config: AppConfig, network_scanner: NetworkScanner, data_repository: DataRepository, mac_repository: MacRepository):
        self.config = config
        self.network_scanner = network_scanner
        self.data_repository = data_repository
        self.mac_repository = mac_repository
        
        self.scanning_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
        self.is_scanning = False
        
        self.last_scan_time: Optional[datetime] = None
        self.scan_error: Optional[str] = None
        self.last_scan_results = []
        
        self.basic_scan_interval = 60  # 1 minute
        self.full_scan_interval = 300  # 5 minutes
        
    def start(self, delay: int = 0):
        """Start the background scanning service."""
        self.stop_event.clear()
        self.scanning_thread = threading.Thread(target=self._scan_loop, args=(delay,), daemon=True)
        self.scanning_thread.start()
        
    def stop(self):
        """Stop the background scanning service."""
        self.stop_event.set()
        if self.scanning_thread:
            self.scanning_thread.join(timeout=5)    
        
    def get_status(self) -> dict[str, str | bool | None]:
        """Get current scanner status."""
        return {
            'is_scanning': self.is_scanning,
            'last_scan_time': self.last_scan_time.isoformat() if self.last_scan_time else None,
        }
        
    def get_latest_devices(self) -> List[Device]:
        """Get the latest scan results."""
        if not self.last_scan_results:
            return []
        return self.data_repository.get_known_unknown_devices(self.last_scan_results)
        
    def _scan_loop(self, delay: int = 0):
        """Main scanning loop that runs in background thread."""
        
        if delay > 0:
            if self.stop_event.wait(timeout=delay):
                return 
        
        basic_scan_counter = 0
        full_scan_counter = 0
        
        # Perform initial full scan
        self._perform_scan(full_scan=True)
        
        while not self.stop_event.is_set():
            if self.stop_event.wait(timeout=60):
                break
                
            basic_scan_counter += 60
            full_scan_counter += 60
            
            # Perform full scan every 5 minutes
            if full_scan_counter >= self.full_scan_interval:
                self._perform_scan(full_scan=True)
                full_scan_counter = 0
                # Reset basic scan counter so it doesn't run immediately after full scan
                basic_scan_counter = 0
                
            # Perform basic scan every minute
            elif basic_scan_counter >= self.basic_scan_interval:
                self._perform_scan(full_scan=False)
                basic_scan_counter = 0
                    
                
    def _perform_scan(self, full_scan: bool = False):
        """Perform a network scan."""
        if self.is_scanning:
            return
            
        self.is_scanning = True
        self.scan_error = None
        
        if full_scan:
            scan_options = ScanOptions.full_scan()
            save_func = self.data_repository.save_full_scan
        else:
            scan_options = ScanOptions.mac_only()
            save_func = self.data_repository.save_mac_scan                
        
        scanned_devices = self.network_scanner.scan_network(scan_options)
        
        if scanned_devices:
            for device in scanned_devices:
                if device.mac_address:
                    save_func(device)
                        
            self.last_scan_results = scanned_devices             
        else:
            self.last_scan_results = []
            
        self.last_scan_time = datetime.now()
        self.is_scanning = False
