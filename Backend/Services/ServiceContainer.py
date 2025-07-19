from typing import Any

from mac_vendor_lookup import MacLookup  # type: ignore

from Backend.Services.AppConfiguration import AppConfig
from Backend.Services.BackgroundScanner import BackgroundScanner
from Backend.Services.DataPersistence import DatabaseConnection, DataRepository, DiscoveryRepository, MacRepository, PortRepository
from Backend.Services.Discovery.MdnsDiscoverer import MdnsDiscoverer
from Backend.Services.Discovery.NetBiosDiscoverer import NetBiosDiscoverer
from Backend.Services.Discovery.UpnpDiscoverer import UpnpDiscoverer
from Backend.Services.Enrichment.HostnameResolver import HostnameResolver
from Backend.Services.Enrichment.MacVendorLookup import MacVendorLookup
from Backend.Services.Enrichment.OperatingSystemLookup import OperatingSystemLookup
from Backend.Services.Networking.MacResolver import MacResolver
from Backend.Services.Networking.NetworkPinger import NetworkPinger
from Backend.Services.Networking.PortScanner import PortScanner
from Backend.Services.NetworkScanner import NetworkScanner
from Backend.Services.ServiceDetection.GenericBannerDetector import GenericBannerDetector
from Backend.Services.ServiceDetection.HttpServiceDetector import HttpServiceDetector
from Backend.Services.ServiceDetection.SshServiceDetector import SshServiceDetector


class ServiceContainer:
    """
    Dependency injection container for the network monitor services.
    """
    
    def __init__(self, config_file_path: str) -> None:
        self._config_file_path = config_file_path
        self._services = self._initialize_services()
    
    def _initialize_services(self) -> dict[str, Any]:
        """Initialize all services with proper dependency injection."""
        
        # External Dependencies
        mac_lookup = MacLookup()  # type: ignore
        
        # Application Configuration
        config = AppConfig(self._config_file_path)
        
        # Networking Services
        pinger = NetworkPinger(config)
        mac_resolver = MacResolver(config)
        port_scanner = PortScanner(config)
        
        # Enrichment Services
        hostname_resolver = HostnameResolver(config)
        vendor_lookup = MacVendorLookup(mac_lookup)
        os_lookup = OperatingSystemLookup()
        
        # Service Detection Services
        http_detector = HttpServiceDetector(config)
        ssh_detector = SshServiceDetector(config)
        banner_detector = GenericBannerDetector(config)
        
        # Discovery Services
        netbios_discoverer = NetBiosDiscoverer(config)
        upnp_discoverer = UpnpDiscoverer(config)
        mdns_discoverer = MdnsDiscoverer(config)
                
        # Data Persistence Services
        database_connection = DatabaseConnection(config)
        data_repository = DataRepository(database_connection)
        discovery_repository = DiscoveryRepository(database_connection)
        mac_repository = MacRepository(database_connection)
        port_repository = PortRepository(database_connection)
        
        # Main Orchestrator
        network_scanner = NetworkScanner(
            config, pinger, mac_resolver, port_scanner,
            http_detector, ssh_detector, banner_detector,
            hostname_resolver, vendor_lookup, os_lookup,
            netbios_discoverer, upnp_discoverer, mdns_discoverer
        )
        
        # Background Scanner
        background_scanner = BackgroundScanner(
            config, network_scanner, data_repository, mac_repository
        )
        
        return {
            'config': config,
            'network_scanner': network_scanner,
            'background_scanner': background_scanner,
            'database_connection': database_connection,
            'data_repository': data_repository,
            'discovery_repository': discovery_repository,
            'mac_repository': mac_repository,
            'port_repository': port_repository,
            
            'pinger': pinger,
            'mac_resolver': mac_resolver,
            'port_scanner': port_scanner,
            
            'hostname_resolver': hostname_resolver,
            'vendor_lookup': vendor_lookup,
            'os_detector': os_lookup,
            
            'http_detector': http_detector,
            'ssh_detector': ssh_detector,
            'banner_detector': banner_detector,
            
            'netbios_discoverer': netbios_discoverer,
            'upnp_discoverer': upnp_discoverer,
            'mdns_discoverer': mdns_discoverer,
        }
    
    def config(self) -> AppConfig:
        return self._services['config']
    def network_scanner(self) -> NetworkScanner:
        return self._services['network_scanner']
    def background_scanner(self) -> BackgroundScanner:
        return self._services['background_scanner']
    def database_connection(self) -> DatabaseConnection:
        return self._services['database_connection']
    def data_repository(self) -> DataRepository:
        return self._services['data_repository']
    def discovery_repository(self) -> DiscoveryRepository:
        return self._services['discovery_repository']
    def mac_repository(self) -> MacRepository:
        return self._services['mac_repository']
    def port_repository(self) -> PortRepository:
        return self._services['port_repository']
    def pinger(self) -> NetworkPinger:
        return self._services['pinger']
    def mac_resolver(self) -> MacResolver:
        return self._services['mac_resolver']
    def port_scanner(self) -> PortScanner:
        return self._services['port_scanner']
    def hostname_resolver(self) -> HostnameResolver:
        return self._services['hostname_resolver']
    def vendor_lookup(self) -> MacVendorLookup:
        return self._services['vendor_lookup']
    def os_detector(self) -> OperatingSystemLookup:
        return self._services['os_detector']
    def http_detector(self) -> HttpServiceDetector:
        return self._services['http_detector']
    def ssh_detector(self) -> SshServiceDetector:
        return self._services['ssh_detector']
    def banner_detector(self) -> GenericBannerDetector:
        return self._services['banner_detector']
    def netbios_discoverer(self) -> NetBiosDiscoverer:
        return self._services['netbios_discoverer']
    def upnp_discoverer(self) -> UpnpDiscoverer:
        return self._services['upnp_discoverer']
    def mdns_discoverer(self) -> MdnsDiscoverer:
        return self._services['mdns_discoverer']
    
    
    def close(self) -> None:
        """Clean up resources."""
        if self.background_scanner():
            self.background_scanner().stop()
        if self.database_connection():
            self.database_connection().close()
