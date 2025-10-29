import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

from sqlalchemy import text

from app import config
from app.database import Database
from app.models import Mac
from app.objects import AddressData, ScanOptions
from app.services.interfaces import (DiscoveryServiceInterface,
                                     MacServiceInterface, PingServiceInterface,
                                     PortServiceInterface,
                                     ProtocolServiceInterface,
                                     ScanServiceInterface)

BANNER_SERVICE_NAMES = ["telnet", "smtp", "pop3", "imap", "ftp"]
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3389, 5900, 8080]
HTTP_PORTS = [80, 443, 8080, 8443]
HTTP_SERVICE_NAME = "http"
SSH_PORT = 22
SSH_SERVICE_NAME = "ssh"
MAX_MESSAGE_LENGTH = 80
        
class ScanService(ScanServiceInterface):
    """Service for handling network scanning operations."""

    def __init__(
        self,
        database: Database,
        ping_service: PingServiceInterface,
        mac_service: MacServiceInterface,
        port_service: PortServiceInterface,
        discovery_service: DiscoveryServiceInterface,
        protocol_service: ProtocolServiceInterface,
    ) -> None:
        self.database = database
        self.ping_service = ping_service
        self.mac_service = mac_service
        self.port_service = port_service
        self.discovery_service = discovery_service
        self.protocol_service = protocol_service
        self.print_lock = threading.Lock()

    def save_mac_scan(self, address_data: AddressData) -> None:
        """Save or update device data for mac only scan."""
        if address_data.mac_address:
             self.mac_service.save_mac(address_data, True)   
    
    def save_full_scan(self, address_data: AddressData) -> None:
        """Save or update device data for full scan."""
        saved_mac = None
        if address_data.mac_address:
            saved_mac = self.mac_service.save_mac(address_data, False)
        if saved_mac and address_data.open_ports:
            self.port_service.save_port(saved_mac, address_data.open_ports, address_data.services_info)      
        if saved_mac and address_data.discovered_info:
            self.discovery_service.save_discoveries(saved_mac, address_data.discovered_info)
            
    def get_latest_scan_date(self) -> datetime | None:
        """Get the date of the latest scan."""
        latest_scan = self.database.select_all(Mac).order_by(text("last_seen DESC")).first()
        if latest_scan:
            return latest_scan.last_seen
        return None

    def scan_network(self, scan_options: ScanOptions) -> list[AddressData]:
        """Scan the configured network range."""        
        subnet = config.subnet
        min_ip = config.min_scan_ip
        max_ip = config.max_scan_ip
        max_threads = config.max_threads
        
        devices: list[AddressData] = []
        ip_range: list[str] = [f"{subnet}.{i}" for i in range(min_ip, max_ip + 1)]

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip, scan_options) for ip in ip_range]
            for future in as_completed(futures):
                device: AddressData | None = future.result()
                if device is not None:
                    devices.append(device)
                    
        self._print_status("Scanning completed")
        return devices
    
    def scan_ip(self, ip_address: str, scan_options: ScanOptions) -> AddressData | None:
        """Scan a specific IP address."""
        scan_result = AddressData(ip_address=ip_address)
        
        # Step 1: Ping the IP
        self._print_status(f"{ip_address} Scanning started")
        success, scan_result.ping_time_ms, ping_out = self.ping_service.ping(ip_address)
        if not success:
            return None
                
        # Step 2: MAC resolution
        if scan_options.mac_resolution:
            self._print_status(f"{ip_address} MAC resolution started")
            arp_result = self.mac_service.resolve_mac_address(ip_address)
            if arp_result:
                scan_result.mac_address, scan_result.arp_time_ms = arp_result
        
        # Step 3: Extract TTL from ping output
        if scan_options.ttl_resolution and ping_out:
            self._print_status(f"{ip_address} Extracting TTL from ping output")
            scan_result.ttl = self.ping_service.get_ttl_from_ping(ping_out)
        
        # Step 4: Resolve hostname
        if scan_options.hostname_resolution:
            self._print_status(f"{ip_address} Resolving hostname")
            scan_result.hostname = self.ping_service.get_hostname(ip_address)
        
        # Step 5: MAC vendor lookup
        if scan_options.mac_vendor_lookup and scan_result.mac_address:
            self._print_status(f"{ip_address} Looking up MAC vendor")
            scan_result.mac_vendor = self.mac_service.get_vendor_from_mac(scan_result.mac_address)
        
        # Step 6: OS detection
        if scan_options.os_detection and scan_result.ttl:
            self._print_status(f"{ip_address} Detecting OS from TTL")
            scan_result.os_guess = self.ping_service.get_os_from_ttl(scan_result.ttl)
        
        # Step 7: Port scanning
        if scan_options.port_scan:
            self._print_status(f"{ip_address} Port scanning started")
            scan_result.open_ports = self.port_service.scan_ports(ip_address, COMMON_PORTS)
        
        #Step 8: Service detection
        for port_info in scan_result.open_ports:
            self._print_status(f"{ip_address}:{port_info.number} Service detection started")
            service_name = port_info.service.lower() if port_info.service else "unknown"
        
            # Step 8.1: HTTP detection
            if scan_options.detect_http and (port_info.number in HTTP_PORTS or HTTP_SERVICE_NAME in service_name):
                self._print_status(f"{ip_address}:{port_info.number} Checking HTTP service")
                result = self.protocol_service.detect_http(ip_address, port_info.number)
                if result:
                    scan_result.services_info[port_info.number] = result

            # Step 8.2: SSH detection
            if scan_options.detect_ssh and (port_info.number == SSH_PORT or SSH_SERVICE_NAME in service_name):
                self._print_status(f"{ip_address}:{port_info.number} Checking SSH service")
                result = self.protocol_service.detect_ssh(ip_address, port_info.number)
                if result:
                    scan_result.services_info[port_info.number] = result

            # Step 8.3: Generic banner detection
            if scan_options.detect_banners and service_name in BANNER_SERVICE_NAMES:
                self._print_status(f"{ip_address}:{port_info.number} Checking banner")
                result = self.protocol_service.detect_banner(ip_address, port_info.number, service_name)
                if result:
                    scan_result.services_info[port_info.number] = result

        # Step 9: Device discovery
        if scan_options.discover_netbios:
            self._print_status(f"{ip_address} Discovering NetBIOS devices")
            discovery_info = self.discovery_service.discover_netbios(ip_address)
            if discovery_info:
                scan_result.discovered_info.append(discovery_info)
        
        # Step 10: UPnP discovery
        if scan_options.discover_upnp:
            self._print_status(f"{ip_address} Discovering UPnP devices")
            discovery_info = self.discovery_service.discover_upnp(ip_address)
            if discovery_info:
                scan_result.discovered_info.append(discovery_info)
        
        # Step 11: mDNS discovery
        if scan_options.discover_mdns:
            self._print_status(f"{ip_address} Discovering mDNS devices")
            discovery_info = self.discovery_service.discover_mdns(ip_address)
            if discovery_info:
                scan_result.discovered_info.append(discovery_info)
                        
        return scan_result
    
    def _print_status(self, message: str) -> None:
        if len(message) > MAX_MESSAGE_LENGTH:
            message = message[:MAX_MESSAGE_LENGTH - 3] + "..."
        
        with self.print_lock:
            message = "Scan Service: " + message
            message = datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + message
            message = message.ljust(MAX_MESSAGE_LENGTH)
            
            print(message, end='\r', flush=True)