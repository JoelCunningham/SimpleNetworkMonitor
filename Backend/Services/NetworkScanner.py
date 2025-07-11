import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional, Tuple

from Backend.Constants import (BANNER_SERVICE_NAMES, COMMON_PORTS, HTTP_PORTS,
                       HTTP_SERVICE_NAME, SSH_PORT, SSH_SERVICE_NAME, TTL_REGEX)
from Backend.Objects.AddressData import AddressData
from Backend.Objects.DiscoveryInfo import DiscoveryInfo
from Backend.Objects.Injectable import Injectable
from Backend.Objects.PortInfo import PortInfo
from Backend.Objects.ScanOptions import ScanOptions
from Backend.Objects.ServiceInfo import ServiceInfo
from Backend.Services.AppConfiguration import AppConfig
from Backend.Services.Discovery.MdnsDiscoverer import MdnsDiscoverer
from Backend.Services.Discovery.NetBiosDiscoverer import NetBiosDiscoverer
from Backend.Services.Discovery.UpnpDiscoverer import UpnpDiscoverer
from Backend.Services.Enrichment.HostnameResolver import HostnameResolver
from Backend.Services.Enrichment.MacVendorLookup import MacVendorLookup
from Backend.Services.Enrichment.OperatingSystemLookup import OperatingSystemLookup
from Backend.Services.Networking.MacResolver import MacResolver
from Backend.Services.Networking.NetworkPinger import NetworkPinger
from Backend.Services.Networking.PortScanner import PortScanner
from Backend.Services.ServiceDetection.GenericBannerDetector import GenericBannerDetector
from Backend.Services.ServiceDetection.HttpServiceDetector import HttpServiceDetector
from Backend.Services.ServiceDetection.SshServiceDetector import SshServiceDetector


class NetworkScanner(Injectable):
    """Main network scanning service."""
    
    def __init__(self, 
                 config: AppConfig,
                 pinger: NetworkPinger,
                 mac_resolver: MacResolver,
                 port_scanner: PortScanner,
                 http_detector: HttpServiceDetector,
                 ssh_detector: SshServiceDetector,
                 banner_detector: GenericBannerDetector,
                 hostname_resolver: HostnameResolver, 
                 vendor_lookup: MacVendorLookup, 
                 os_lookup: OperatingSystemLookup,
                 netbios_discoverer: NetBiosDiscoverer,
                 upnp_discoverer: UpnpDiscoverer,
                 mdns_discoverer: MdnsDiscoverer) -> None:
        self._config = config
        self._pinger = pinger
        self._mac_resolver = mac_resolver
        self._port_scanner = port_scanner
        self._http_detector = http_detector
        self._ssh_detector = ssh_detector
        self._banner_detector = banner_detector
        self._hostname_resolver = hostname_resolver
        self._vendor_lookup = vendor_lookup
        self._os_lookup = os_lookup
        self._netbios_discoverer = netbios_discoverer
        self._upnp_discoverer = upnp_discoverer
        self._mdns_discoverer = mdns_discoverer
    
    def scan_network(self, scan_options: Optional[ScanOptions] = None) -> List[AddressData]:
        """Scan the configured network range."""        
        subnet = self._config.network.subnet()
        min_ip = self._config.network.min_ip()
        max_ip = self._config.network.max_ip()
        max_threads = self._config.network.max_threads()
        
        if scan_options is None:
            scan_options = self._get_config_based_scan_options()
        
        devices: List[AddressData] = []
        ip_range: List[str] = [f"{subnet}.{i}" for i in range(min_ip, max_ip + 1)]

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip, scan_options) for ip in ip_range]
            for future in as_completed(futures):
                device: Optional[AddressData] = future.result()
                if device is not None:
                    devices.append(device)
        return devices
    
    def _get_config_based_scan_options(self) -> ScanOptions:
        """Create scan options based on current configuration."""
        feature = self._config.feature
        return ScanOptions(
            mac_resolution=feature.mac_resolution_enabled(),
            ttl_resolution=feature.ttl_resolution_enabled(),
            hostname_resolution=feature.hostname_resolution_enabled(),
            mac_vendor_lookup=feature.mac_vendor_lookup_enabled(),
            os_detection=feature.os_detection_enabled(),
            port_scan=feature.port_scan_enabled(),
            detect_http=feature.detect_http_enabled(),
            detect_ssh=feature.detect_ssh_enabled(),
            detect_banners=feature.detect_banners_enabled(),
            discover_netbios=feature.discover_netbios_enabled(),
            discover_upnp=feature.discover_upnp_enabled(),
            discover_mdns=feature.discover_mdns_enabled()
        )
    
    def scan_ip(self, ip_address: str, scan_options: Optional[ScanOptions] = None) -> Optional[AddressData]:
        """Scan a specific IP address."""
        # Use provided scan options or default to config-based scanning
        if scan_options is None:
            scan_options = self._get_config_based_scan_options()
                
        # Initialize data containers
        mac_address: Optional[str] = None
        arp_time_ms: int = 0
        ttl: Optional[int] = None
        hostname: Optional[str] = None
        mac_vendor: Optional[str] = None
        os_guess: Optional[str] = None
        open_ports: List[PortInfo] = []
        services_info: Dict[int, ServiceInfo] = {}
        discovered_info: List[DiscoveryInfo] = []
        
        # Step 1: Ping the IP
        print(f"{ip_address} Scanning started")
        success, ping_time_ms, ping_out = self._pinger.ping(ip_address)
        if not success:
            return None
                
        # Step 2: MAC resolution
        if scan_options.mac_resolution:
            print(f"{ip_address} MAC resolution started")
            arp_result = self._mac_resolver.resolve_mac_address(ip_address)
            if arp_result:
                mac_address, arp_time_ms = arp_result
        
        # Step 3: Extract TTL from ping output
        if scan_options.ttl_resolution and ping_out:
            print(f"{ip_address} Extracting TTL from ping output")
            ttl = self._extract_ttl_from_ping_output(ping_out)
        
        # Step 4: Device enrichment (hostname, vendor, OS detection)
        if scan_options.hostname_resolution:
            print(f"{ip_address} Resolving hostname")
            hostname = self._hostname_resolver.resolve_hostname(ip_address)
        
        if scan_options.mac_vendor_lookup and mac_address:
            print(f"{ip_address} Looking up MAC vendor")
            mac_vendor = self._vendor_lookup.get_vendor(mac_address)
        
        if scan_options.os_detection and ttl:
            print(f"{ip_address} Detecting OS from TTL")
            os_guess = self._os_lookup.detect_from_ttl(ttl)
        
        # Step 5: Port scanning
        if scan_options.port_scan:
            print(f"{ip_address} Port scanning started")
            open_ports = self._port_scanner.scan_ports(ip_address, COMMON_PORTS)
        
        # Step 6: Service detection
        for port_info in open_ports:
            print(f"{ip_address}:{port_info.port} Service detection started")
            service_info: Optional[ServiceInfo] = None
            service_name = port_info.service.lower() if port_info.service else "unknown"
        
            # HTTP detection
            if scan_options.detect_http and (port_info.port in HTTP_PORTS or HTTP_SERVICE_NAME in service_name):
                print(f"{ip_address}:{port_info.port} Checking HTTP service")
                service_info = self._http_detector.detect_service(ip_address, port_info.port)
            
            # SSH detection
            if scan_options.detect_ssh and (port_info.port == SSH_PORT or SSH_SERVICE_NAME in service_name):
                print(f"{ip_address}:{port_info.port} Checking SSH service")
                service_info = self._ssh_detector.detect_service(ip_address, port_info.port)
            
            # Generic banner grabbing
            if scan_options.detect_banners and service_name in BANNER_SERVICE_NAMES:
                print(f"{ip_address}:{port_info.port} Checking banner")
                banner = self._banner_detector.grab_banner(ip_address, port_info.port)
                if banner:
                    service_info = ServiceInfo(
                        service_name=service_name,
                        extra_info=banner
                    )            
            
            if service_info:
                services_info[port_info.port] = service_info
        
        # Step 7: Device discovery
        if scan_options.discover_netbios:
            print(f"{ip_address} Discovering NetBIOS devices")
            discovery_info = self._netbios_discoverer.discover(ip_address)
            if discovery_info:
                discovered_info.append(discovery_info)
        
        if scan_options.discover_upnp:
            print(f"{ip_address} Discovering UPnP devices")
            discovery_info = self._upnp_discoverer.discover(ip_address)
            if discovery_info:
                discovered_info.append(discovery_info)
        
        if scan_options.discover_mdns:
            print(f"{ip_address} Discovering mDNS devices")
            discovery_info = self._mdns_discoverer.discover(ip_address)
            if discovery_info:
                discovered_info.append(discovery_info)
        
        return AddressData(
            mac_address=mac_address,
            ip_address=ip_address,
            ping_time_ms=ping_time_ms,
            arp_time_ms=arp_time_ms,
            hostname=hostname,
            mac_vendor=mac_vendor,
            os_guess=os_guess,
            ttl=ttl,
            open_ports=open_ports,
            services_info=services_info,
            discovered_info=discovered_info
        )
    
    def _extract_ttl_from_ping_output(self, ping_output: str) -> Optional[int]:
        """Extract TTL value from ping output."""
        try:
            ttl_match = re.search(TTL_REGEX, ping_output)
            if ttl_match:
                return int(ttl_match.group(1))
        except (ValueError, AttributeError):
            pass
        return None
    
    def get_scan_summary(self, address_data: AddressData) -> Tuple[Optional[List[str]], Optional[List[str]], Optional[List[str]]]:
        """Get a summary of scan results for display."""  
        open_ports, services, discovered_info = None, None, None
        
        if address_data.open_ports:
            open_ports = [f"{p.port}/{p.protocol}" for p in address_data.open_ports]
        
        if address_data.services_info:
            services = [f"{port}:{service.service_name}" for port, service in address_data.services_info.items()]
        
        if address_data.discovered_info:
            discovered_info = [f"{d.protocol}:{d.device_type}" for d in address_data.discovered_info if d.device_type]
        
        return open_ports, services, discovered_info
