from typing import Callable, Generic, Optional, TypeVar

import Constants
from Objects.Injectable import Injectable
from Services.AdvancedDataService import AdvancedDataService
from Services.PortScannerService import PortScannerService
from Services.ServiceDetectionService import ServiceDetectionService
from Services.AppConfig import AppConfig
from Services.Database import Database
from Services.EnrichmentService import EnrichmentService
from Services.MacService import MacService
from Services.NetworkScanner import NetworkScanner
from Services.DiscoveryService import DiscoveryService

T = TypeVar('T', bound=Injectable)

class Lazy(Generic[T]):
    """Simple lazy loader for dependencies."""
    
    def __init__(self, factory: Callable[[], T]):
        self._factory = factory
        self._instance: Optional[T] = None
    
    def get(self) -> T:
        if self._instance is None:
            self._instance = self._factory()
        return self._instance
    
    def dispose(self):
        if self._instance:
            try:
                self._instance.dispose()
            except Exception:
                pass  
        self._instance = None


class Container:
    """Simple dependency injection container with lazy loading."""
    
    config: Lazy[AppConfig]
    database: Lazy[Database]
    scanner_service: Lazy[NetworkScanner]
    advanced_data_service: Lazy[AdvancedDataService]
    mac_service: Lazy[MacService]
    enrichment_service: Lazy[EnrichmentService]
    port_scanner: Lazy[PortScannerService]
    service_detector: Lazy[ServiceDetectionService]
    discovery_service: Lazy[DiscoveryService]
    
    def __init__(self):
        self.config = Lazy(lambda: AppConfig(Constants.DEFAULT_CONFIG_PATH))
        self.database = Lazy(lambda: Database(self.config.get()))
        self.advanced_data_service = Lazy(lambda: AdvancedDataService(self.database.get()))
        self.scanner_service = Lazy(lambda: NetworkScanner(self.config.get(), self.enrichment_service.get(), self.port_scanner.get(), self.service_detector.get(), self.discovery_service.get()))
        self.mac_service = Lazy(lambda: MacService(self.database.get(), self.advanced_data_service.get()))
        self.enrichment_service = Lazy(lambda: EnrichmentService(self.config.get()))
        self.port_scanner = Lazy(lambda: PortScannerService(self.config.get()))
        self.service_detector = Lazy(lambda: ServiceDetectionService(self.config.get()))
        self.discovery_service = Lazy(lambda: DiscoveryService(self.config.get()))
    
    def dispose(self):
        self.config.dispose()
        self.database.dispose()
        self.scanner_service.dispose()
        self.advanced_data_service.dispose()
        self.mac_service.dispose()
        self.enrichment_service.dispose()
        self.port_scanner.dispose()
        self.service_detector.dispose()
        self.discovery_service.dispose()
