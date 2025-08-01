"""
Service factory for creating properly configured service instances.

Handles the complex dependency injection for services with many dependencies.
"""
from flask import Flask


class Container:
    """Factory class for creating properly configured service instances."""
    app = None
    
    _scan_controller = None
    _device_controller = None
    
    _scan_service = None
    _mac_service = None
    _device_service = None
    
    def init(self, app: Flask):
        """Initialize the container with the Flask app."""
        self.app = app
    
    def mac_service(self):
        """Get or create a shared MacService instance."""
        from app.services.mac_service import MacService
        
        if self._mac_service is None:
            self._mac_service = MacService()
        return self._mac_service
    
    def device_service(self):
        """Get or create a DeviceService instance with all dependencies."""
        from app.services.device_service import DeviceService
        
        if self._device_service is None:
            mac_service = self.mac_service()
            self._device_service = DeviceService(mac_service)
        return self._device_service
    
    def scan_service(self):
        """Get or create a NetworkScannerService instance with all dependencies."""
        from app.services.discovery_service import DiscoveryService
        from app.services.ping_service import PingService
        from app.services.port_service import PortService
        from app.services.protocol_service import ProtocolService
        from app.services.scan_service import ScanService
        
        if self._scan_service is None:
            ping_service = PingService()
            mac_service = self.mac_service() 
            port_service = PortService()
            discovery_service = DiscoveryService()
            protocol_service = ProtocolService()
            
            self._scan_service = ScanService(
                ping_service=ping_service,
                mac_service=mac_service,
                port_service=port_service,
                discovery_service=discovery_service,
                protocol_service=protocol_service
            )
        return self._scan_service
    
    def scan_controller(self):
        """Get or create a BackgroundScannerService instance."""
        from app.controllers.scan_controller import ScanController
        
        if self.app is None:
            raise RuntimeError("Container must be initialized with an app instance")
        
        if self._scan_controller is None:
            self._scan_controller = ScanController(
                scan_service=self.scan_service(),
                device_service=self.device_service(),
                app=self.app
            )
        return self._scan_controller

    def device_controller(self):
        """Get or create a DeviceController instance."""
        from app.controllers.device_controller import DeviceController
        
        if self.app is None:
            raise RuntimeError("Container must be initialized with an app instance")
        
        if self._device_controller is None:
            self._device_controller = DeviceController(
                device_service=self.device_service()
            )
        return self._device_controller