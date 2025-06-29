"""Dependency injection container for refactored services."""
from typing import Dict, Any

# Configuration Services
from Services.Configuration.ConfigurationServices import (
    ConfigurationLoader, ConfigurationValidator, NetworkMonitorConfiguration
)

# Networking Services  
from Services.Networking.PingAndArpServices import NetworkPinger, ArpResolver
from Services.Networking.PortScannerService import PortScannerService

# Enrichment Services
from Services.Enrichment.DeviceEnrichmentServices import (
    HostnameResolver, MacVendorLookupService, OperatingSystemDetector, DeviceEnrichmentService
)

# Service Detection Services
from Services.ServiceDetection.ServiceDetectors import (
    HttpServiceDetector, SshServiceDetector, GenericBannerGrabber, ServiceDetectionOrchestrator
)

# Discovery Services
from Services.Discovery.DiscoveryProtocols import (
    NetBiosDiscoveryProtocol, UpnpDiscoveryProtocol, MdnsDiscoveryProtocol, DeviceDiscoveryService
)

# Data Persistence Services
from Services.DataPersistence.DataPersistenceServices import (
    DatabaseConnection, DeviceRepository, ScanDataRepository
)

# Main Orchestrator
from Services.NetworkScanOrchestrator import NetworkScanOrchestrator

# Interface Implementations
from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.INetworkScanning import INetworkScanner
from Interfaces.IDataPersistence import IDatabaseConnection, IDeviceRepository, IScanDataRepository


class ServiceContainer:
    """
    Dependency injection container for the network monitor services.
    
    This container follows SOLID principles:
    - Single Responsibility: Each service has one clear responsibility
    - Open/Closed: Services can be extended through interfaces
    - Liskov Substitution: All implementations follow their interface contracts  
    - Interface Segregation: Interfaces are focused and specific
    - Dependency Inversion: Services depend on abstractions, not concretions
    """
    
    def __init__(self, config_file_path: str) -> None:
        self._config_file_path = config_file_path
        self._services: Dict[str, Any] = {}
        self._initialize_services()
    
    def _initialize_services(self) -> None:
        """Initialize all services with proper dependency injection."""
        
        # Configuration Services
        config_loader = ConfigurationLoader()
        config_validator = ConfigurationValidator()
        configuration = NetworkMonitorConfiguration(
            self._config_file_path, config_loader, config_validator
        )
        
        # Networking Services
        pinger = NetworkPinger(configuration)
        arp_resolver = ArpResolver(configuration)
        port_scanner = PortScannerService(configuration)
        
        # Enrichment Services
        hostname_resolver = HostnameResolver(configuration)
        mac_vendor_lookup = MacVendorLookupService()
        os_detector = OperatingSystemDetector()
        device_enrichment = DeviceEnrichmentService(
            hostname_resolver, mac_vendor_lookup, os_detector, configuration
        )
        
        # Service Detection Services
        http_detector = HttpServiceDetector(configuration)
        ssh_detector = SshServiceDetector(configuration)
        banner_grabber = GenericBannerGrabber(configuration)
        service_orchestrator = ServiceDetectionOrchestrator(
            configuration, http_detector, ssh_detector, banner_grabber
        )
        
        # Discovery Services
        netbios_protocol = NetBiosDiscoveryProtocol(configuration)
        upnp_protocol = UpnpDiscoveryProtocol(configuration)
        mdns_protocol = MdnsDiscoveryProtocol(configuration)
        
        discovery_service = DeviceDiscoveryService(configuration)
        discovery_service.register_protocol(netbios_protocol)
        discovery_service.register_protocol(upnp_protocol)
        discovery_service.register_protocol(mdns_protocol)
        
        # Data Persistence Services
        database_connection = DatabaseConnection(configuration)
        device_repository = DeviceRepository(database_connection)
        scan_data_repository = ScanDataRepository(database_connection)
        
        # Main Orchestrator
        network_scanner = NetworkScanOrchestrator(
            configuration, pinger, arp_resolver, port_scanner,
            device_enrichment, discovery_service, service_orchestrator
        )
        
        # Store services for retrieval
        self._services.update({
            # Main interfaces
            'configuration': configuration,
            'network_scanner': network_scanner,
            'database_connection': database_connection,
            'device_repository': device_repository,
            'scan_data_repository': scan_data_repository,
            
            # Individual services
            'pinger': pinger,
            'arp_resolver': arp_resolver,
            'port_scanner': port_scanner,
            'device_enrichment': device_enrichment,
            'discovery_service': discovery_service,
            'service_orchestrator': service_orchestrator,
            'hostname_resolver': hostname_resolver,
            'mac_vendor_lookup': mac_vendor_lookup,
            'os_detector': os_detector,
            'http_detector': http_detector,
            'ssh_detector': ssh_detector,
            'banner_grabber': banner_grabber
        })
    
    def get_configuration(self) -> IConfigurationProvider:
        """Get the configuration provider."""
        return self._services['configuration']
    
    def get_network_scanner(self) -> INetworkScanner:
        """Get the main network scanner."""
        return self._services['network_scanner']
    
    def get_database_connection(self) -> IDatabaseConnection:
        """Get the database connection."""
        return self._services['database_connection']
    
    def get_device_repository(self) -> IDeviceRepository:
        """Get the device repository."""
        return self._services['device_repository']
    
    def get_scan_data_repository(self) -> IScanDataRepository:
        """Get the scan data repository."""
        return self._services['scan_data_repository']
    
    def get_service(self, service_name: str) -> Any:
        """Get a specific service by name."""
        return self._services.get(service_name)
    
    def close(self) -> None:
        """Clean up resources."""
        database_connection = self._services.get('database_connection')
        if database_connection:
            database_connection.close()
