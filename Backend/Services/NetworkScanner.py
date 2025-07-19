from concurrent.futures import ThreadPoolExecutor, as_completed

from Backend.Constants import (BANNER_SERVICE_NAMES, COMMON_PORTS, HTTP_PORTS,
                               HTTP_SERVICE_NAME, SSH_PORT, SSH_SERVICE_NAME)

from Backend.Objects.AddressData import AddressData
from Backend.Objects.Injectable import Injectable
from Backend.Objects.ScanOptions import ScanOptions
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
    
    def scan_network(self, scan_options: ScanOptions) -> list[AddressData]:
        """Scan the configured network range."""        
        subnet = self._config.network.subnet()
        min_ip = self._config.network.min_ip()
        max_ip = self._config.network.max_ip()
        max_threads = self._config.network.max_threads()
        
        devices: list[AddressData] = []
        ip_range: list[str] = [f"{subnet}.{i}" for i in range(min_ip, max_ip + 1)]

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip, scan_options) for ip in ip_range]
            for future in as_completed(futures):
                device: AddressData | None = future.result()
                if device is not None:
                    devices.append(device)
        return devices
    
    def scan_ip(self, ip_address: str, scan_options: ScanOptions) -> AddressData | None:
        """Scan a specific IP address."""
        scan_result = AddressData(ip_address=ip_address)
        
        # Step 1: Ping the IP
        print(f"{ip_address} Scanning started")
        success, scan_result.ping_time_ms, ping_out = self._pinger.ping(ip_address)
        if not success:
            return None
                
        # Step 2: MAC resolution
        if scan_options.mac_resolution:
            print(f"{ip_address} MAC resolution started")
            arp_result = self._mac_resolver.resolve_mac_address(ip_address)
            if arp_result:
                scan_result.mac_address, scan_result.arp_time_ms = arp_result
        
        # Step 3: Extract TTL from ping output
        if scan_options.ttl_resolution and ping_out:
            print(f"{ip_address} Extracting TTL from ping output")
            scan_result.ttl = self._pinger.get_ttl_from_ping_result(ping_out)
        
        # Step 4: Resolve hostname
        if scan_options.hostname_resolution:
            print(f"{ip_address} Resolving hostname")
            scan_result.hostname = self._hostname_resolver.resolve_hostname(ip_address)
        
        # Step 5: MAC vendor lookup
        if scan_options.mac_vendor_lookup and scan_result.mac_address:
            print(f"{ip_address} Looking up MAC vendor")
            scan_result.mac_vendor = self._vendor_lookup.get_vendor(scan_result.mac_address)
        
        # Step 6: OS detection
        if scan_options.os_detection and scan_result.ttl:
            print(f"{ip_address} Detecting OS from TTL")
            scan_result.os_guess = self._os_lookup.detect_from_ttl(scan_result.ttl)
        
        # Step 7: Port scanning
        if scan_options.port_scan:
            print(f"{ip_address} Port scanning started")
            scan_result.open_ports = self._port_scanner.scan_ports(ip_address, COMMON_PORTS)
        
        #Step 8: Service detection
        for port_info in scan_result.open_ports:
            print(f"{ip_address}:{port_info.port} Service detection started")
            service_name = port_info.service.lower() if port_info.service else "unknown"
        
            # Step 8.1: HTTP detection
            if scan_options.detect_http and (port_info.port in HTTP_PORTS or HTTP_SERVICE_NAME in service_name):
                print(f"{ip_address}:{port_info.port} Checking HTTP service")
                result = self._http_detector.detect_service(ip_address, port_info.port)
                if result:
                    scan_result.services_info[port_info.port] = result
            
            # Step 8.2: SSH detection
            if scan_options.detect_ssh and (port_info.port == SSH_PORT or SSH_SERVICE_NAME in service_name):
                print(f"{ip_address}:{port_info.port} Checking SSH service")
                result = self._ssh_detector.detect_service(ip_address, port_info.port)
                if result:
                    scan_result.services_info[port_info.port] = result
            
            # Step 8.3: Generic banner detection
            if scan_options.detect_banners and service_name in BANNER_SERVICE_NAMES:
                print(f"{ip_address}:{port_info.port} Checking banner")
                result = self._banner_detector.grab_banner(ip_address, port_info.port, service_name)
                if result:
                    scan_result.services_info[port_info.port] = result
        
        # Step 9: Device discovery
        if scan_options.discover_netbios:
            print(f"{ip_address} Discovering NetBIOS devices")
            discovery_info = self._netbios_discoverer.discover(ip_address)
            if discovery_info:
                scan_result.discovered_info.append(discovery_info)
        
        # Step 10: UPnP discovery
        if scan_options.discover_upnp:
            print(f"{ip_address} Discovering UPnP devices")
            discovery_info = self._upnp_discoverer.discover(ip_address)
            if discovery_info:
                scan_result.discovered_info.append(discovery_info)
        
        # Step 11: mDNS discovery
        if scan_options.discover_mdns:
            print(f"{ip_address} Discovering mDNS devices")
            discovery_info = self._mdns_discoverer.discover(ip_address)
            if discovery_info:
                scan_result.discovered_info.append(discovery_info)
        
        return scan_result
    
 
    def get_scan_summary(self, address_data: AddressData) -> tuple[list[str] | None, list[str] | None, list[str] | None]:
        """Get a summary of scan results for display."""  
        open_ports, services, discovered_info = None, None, None
        
        if address_data.open_ports:
            open_ports = [f"{p.port}/{p.protocol}" for p in address_data.open_ports]
        
        if address_data.services_info:
            services = [f"{port}:{service.service_name}" for port, service in address_data.services_info.items()]
        
        if address_data.discovered_info:
            discovered_info = [f"{d.protocol}:{d.device_type}" for d in address_data.discovered_info if d.device_type]
        
        return open_ports, services, discovered_info
