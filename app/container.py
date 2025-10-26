"""Simple Dependency Injection Container for SimpleNetworkMonitor"""
import threading
from contextlib import asynccontextmanager
from typing import Any, Type, TypeVar

from fastapi import Request

from app.config import Config
from app.database import Database
from app.services import *
from app.services.interfaces import *

T = TypeVar('T')


class Container:
    """Simple DI container for service management."""
    
    def __init__(self):
        self._services: dict[Type[Any], Any] = {}
        self._config: Config | None = None
        self._database: Database | None = None
    
    def register(self, service_type: Type[T], instance: T) -> 'Container':
        """Register a service instance."""
        self._services[service_type] = instance
        return self
    
    def get(self, service_type: Type[T]) -> T:
        """Get a service instance."""
        if service_type not in self._services:
            raise ValueError(f"Service {service_type.__name__} not registered")
        return self._services[service_type]
    
    def set_config(self, config: Config):
        """Set configuration."""
        self._config = config
    
    def set_database(self, database: Database):
        """Set database."""
        self._database = database


def create_services(config: Config, database: Database) -> Container:
    """Create and register all services."""
    container = Container()
    container.set_config(config)
    container.set_database(database)

    # Create service instances
    ping_service = PingService(config)
    mac_service = MacService(database)
    port_service = PortService(database)
    discovery_service = DiscoveryService(database)
    protocol_service = ProtocolService()
    scan_service = ScanService(database, ping_service, mac_service, port_service, discovery_service, protocol_service)
    scanning_service = ScanningService(scan_service)
    device_service = DeviceService(database, mac_service, scanning_service)
    owner_service = OwnerService(database)
    category_service = CategoryService(database)
    location_service = LocationService(database)

    # Register services
    container.register(Config, config)
    container.register(Database, database)
    container.register(PingServiceInterface, ping_service)
    container.register(MacServiceInterface, mac_service)
    container.register(PortServiceInterface, port_service)
    container.register(DiscoveryServiceInterface, discovery_service)
    container.register(ProtocolServiceInterface, protocol_service)
    container.register(ScanServiceInterface, scan_service)
    container.register(ScanningServiceInterface, scanning_service)
    container.register(DeviceServiceInterface, device_service)
    container.register(OwnerServiceInterface, owner_service)
    container.register(CategoryServiceInterface, category_service)
    container.register(LocationServiceInterface, location_service)

    return container


# FastAPI dependency functions
def get_database(request: Request) -> Database:
    """Get database from request state."""
    return request.app.state.database


def get_mac_service(request: Request) -> MacServiceInterface:
    """Get MAC service from container."""
    return request.app.state.container.get(MacServiceInterface)


def get_ping_service(request: Request) -> PingServiceInterface:
    """Get ping service from container."""
    return request.app.state.container.get(PingServiceInterface)


def get_port_service(request: Request) -> PortServiceInterface:
    """Get port service from container."""
    return request.app.state.container.get(PortServiceInterface)


def get_discovery_service(request: Request) -> DiscoveryServiceInterface:
    """Get discovery service from container."""
    return request.app.state.container.get(DiscoveryServiceInterface)


def get_protocol_service(request: Request) -> ProtocolServiceInterface:
    """Get protocol service from container."""
    return request.app.state.container.get(ProtocolServiceInterface)


def get_scan_service(request: Request) -> ScanServiceInterface:
    """Get scan service from container."""
    return request.app.state.container.get(ScanServiceInterface)


def get_scanning_service(request: Request) -> ScanningServiceInterface:
    """Get scanning service from container."""
    return request.app.state.container.get(ScanningServiceInterface)


def get_device_service(request: Request) -> DeviceServiceInterface:
    """Get device service from container."""
    return request.app.state.container.get(DeviceServiceInterface)


def get_owner_service(request: Request) -> OwnerServiceInterface:
    """Get owner service from container."""
    return request.app.state.container.get(OwnerServiceInterface)


def get_category_service(request: Request) -> CategoryServiceInterface:
    """Get category service from container."""
    return request.app.state.container.get(CategoryServiceInterface)


def get_location_service(request: Request) -> LocationServiceInterface:
    """Get location service from container."""
    return request.app.state.container.get(LocationServiceInterface)


@asynccontextmanager
async def container_lifespan(app: Any):
    """Lifespan manager that sets up the DI container and starts scanning."""
    from app.config import Config

    # Create config and database
    config = Config()
    database = Database(config.database_url)
    
    # Create services container
    container = create_services(config, database)
    
    # Store in app state
    app.state.database = database
    app.state.container = container
    
    # Start background scanning
    scanning_service = container.get(ScanningServiceInterface)
    thread = threading.Thread(target=scanning_service.start_continuous_scan(), args=(scanning_service,), daemon=True)
    thread.start()
    
    try:
        yield
    finally:
        # Cleanup - database will be garbage collected
        pass
