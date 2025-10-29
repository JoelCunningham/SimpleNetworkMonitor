import threading
from datetime import datetime, timedelta

from app import config
from app.common.constants import *
from app.common.objects.address_data import AddressData
from app.common.objects.scan_options import ScanOptions
from app.services.interfaces import (ScanningServiceInterface,
                                     ScanServiceInterface)


class ScanningService(ScanningServiceInterface):
    """Scan services that manages scanning operations."""

    def __init__(self, scan_service: ScanServiceInterface) -> None:
        self.scan_service = scan_service
        
        self.scanning_thread: threading.Thread | None = None
        self.stop_event = threading.Event()
        self.is_scanning = False
        
        self.last_scan_time: datetime | None = None
        self.scan_error: str | None = None
        self.last_scan_results = []
        
        self.basic_scan_interval = config.background_scan_interval_s
        self.full_scan_interval = config.background_full_scan_interval_s
        
    def get_latest_results(self) -> list[AddressData]:
        return self.last_scan_results
        
    def start_continuous_scan(self):
        self.stop_event.clear()
        self.scanning_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scanning_thread.start()
        
    def stop_continuous_scan(self) -> None:
        if self.scanning_thread and self.scanning_thread.is_alive():
            self.stop_event.set()
            self.scanning_thread.join(timeout=5)
    
    def get_last_scan_time(self) -> datetime | None:
        return self.last_scan_time
        
    def _scan_loop(self):
        """Main scanning loop that runs in background thread."""        
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
            print(f"Scan error during {'full' if full_scan else 'basic'} scan: {e}")
        finally:
            self.is_scanning = False
    
 