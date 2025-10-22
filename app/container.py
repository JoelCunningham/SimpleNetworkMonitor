"""
Service factory for creating properly configured service instances.

Handles the complex dependency injection for services with many dependencies.
"""
from typing import Any, Optional

from fastapi import Request, Depends

from app.database import Database
from app.services.interfaces import (CategoryServiceInterface,
                                     DeviceServiceInterface,
                                     DiscoveryServiceInterface,
                                     LocationServiceInterface,
                                     MacServiceInterface,
                                     OwnerServiceInterface,
                                     PingServiceInterface,
                                     PortServiceInterface,
                                     ProtocolServiceInterface,
                                     ScanServiceInterface)


class Container:
    """Factory class for creating properly configured service instances."""
    _database : Optional[Database] = None
    
    _scanning_service: Optional[Any] = None
    _device_controller: Optional[Any] = None
    
    _scan_service: Optional[ScanServiceInterface] = None
    _mac_service: Optional[MacServiceInterface] = None
    _device_service: Optional[DeviceServiceInterface] = None
    _owner_service: Optional[OwnerServiceInterface] = None
    _category_service: Optional[CategoryServiceInterface] = None
    _location_service: Optional[LocationServiceInterface] = None
    _port_service: Optional[PortServiceInterface] = None
    _discovery_service: Optional[DiscoveryServiceInterface] = None
    _protocol_service: Optional[ProtocolServiceInterface] = None
    _ping_service: Optional[PingServiceInterface] = None
    
    def __init__(self, database: Database) -> None:
        self._database = database

    def database(self) -> Database:
        """Get the shared Database instance."""
        if self._database is None:
            raise ValueError("Database instance is not set in the container.")
        return self._database

    def mac_service(self) -> MacServiceInterface:
        """Get or create a shared MacService instance."""
        from app.services.mac_service import MacService

        if self._mac_service is None:
            self._mac_service = MacService(self.database())
        return self._mac_service
    
    def ping_service(self) -> Any:
        """Get or create a PingService instance."""
        from app.services.ping_service import PingService

        if self._ping_service is None:
            self._ping_service = PingService()
        return self._ping_service
    
    def device_service(self) -> DeviceServiceInterface:
        """Get or create a DeviceService instance with all dependencies."""
        from app.services.device_service import DeviceService

        if self._device_service is None:
            self._device_service = DeviceService(
                self.database(),
                self.mac_service(),
                self.scanning_service(),
            )
        return self._device_service
    
    def owner_service(self) -> OwnerServiceInterface:
        """Get or create an OwnerService instance with all dependencies."""
        from app.services.owner_service import OwnerService

        if self._owner_service is None:
            self._owner_service = OwnerService(self.database())
        return self._owner_service
    
    def category_service(self) -> CategoryServiceInterface:
        """Get or create a CategoryService instance."""
        from app.services.category_service import CategoryService

        if self._category_service is None:
            self._category_service = CategoryService(self.database())
        return self._category_service
    
    def location_service(self) -> LocationServiceInterface:
        """Get or create a LocationService instance."""
        from app.services.location_service import LocationService

        if self._location_service is None:
            self._location_service = LocationService(self.database())
        return self._location_service
    
    def scan_service(self) -> ScanServiceInterface:
        """Get or create a NetworkScannerService instance with all dependencies."""
        from app.services.scan_service import ScanService

        if self._scan_service is None:
            self._scan_service = ScanService(
                self.database(),
                self.ping_service(),
                self.mac_service(),
                self.port_service(),
                self.discovery_service(),
                self.protocol_service(),
            )
        return self._scan_service

    def port_service(self) -> PortServiceInterface:
        """Get or create a PortService instance. Tests can inject a fake via `impl`."""
        from app.services.port_service import PortService

        if self._port_service is None:
            self._port_service = PortService(self.database())
        return self._port_service

    def discovery_service(self) -> DiscoveryServiceInterface:
        """Get or create a DiscoveryService instance. Tests can inject a fake via `impl`."""
        from app.services.discovery_service import DiscoveryService

        if self._discovery_service is None:
            self._discovery_service = DiscoveryService(self.database())
        return self._discovery_service

    def protocol_service(self) -> ProtocolServiceInterface:
        """Get or create a ProtocolService instance. Tests can inject a fake via `impl`."""
        from app.services.protocol_service import ProtocolService

        if self._protocol_service is None:
            self._protocol_service = ProtocolService()
        return self._protocol_service
    
    def scanning_service(self) -> Any:
        """Get or create a BackgroundScannerService instance."""
        from app.services.scanning_service import ScanningService

        if self._scanning_service is None:
            self._scanning_service = ScanningService(self.scan_service())
        return self._scanning_service


def get_container(request: Request) -> Container:
    """Return the application Container instance from app.state.

    Designed for use with FastAPI Depends so endpoints and tests can
    obtain or override service providers.
    """
    container = getattr(request.app.state, "container", None)
    if container is None:
        raise RuntimeError("Application container is not initialized")
    return container


def get_device_service(container: Container = Depends(get_container)):
    return container.device_service()


def get_owner_service(container: Container = Depends(get_container)):
    return container.owner_service()


def get_category_service(container: Container = Depends(get_container)):
    return container.category_service()


def get_location_service(container: Container = Depends(get_container)):
    return container.location_service()

