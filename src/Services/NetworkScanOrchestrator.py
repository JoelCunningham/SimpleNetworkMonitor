"""Main network scanning orchestrator service."""
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Dict, Any

import Constants
from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.INetworkScanning import INetworkScanner, INetworkPinger, IArpResolver, IPortScanner
from Interfaces.IEnrichment import IDeviceEnrichmentService
from Interfaces.IServiceDetection import IDeviceDiscoveryService
from Objects.AddressData import AddressData
from Objects.Injectable import Injectable
from Objects.PortInfo import PortInfo
from Objects.ServiceInfo import ServiceInfo
from Services.ServiceDetection.ServiceDetectors import ServiceDetectionOrchestrator


class NetworkScanOrchestrator(INetworkScanner, Injectable):
    """Main orchestrator for network scanning operations."""
    
    def __init__(self, 
                 config_provider: IConfigurationProvider,
                 pinger: INetworkPinger,
                 arp_resolver: IArpResolver,
                 port_scanner: IPortScanner,
                 enrichment_service: IDeviceEnrichmentService,
                 discovery_service: IDeviceDiscoveryService,
                 service_orchestrator: ServiceDetectionOrchestrator) -> None:
        self._config_provider = config_provider
        self._pinger = pinger
        self._arp_resolver = arp_resolver
        self._port_scanner = port_scanner
        self._enrichment_service = enrichment_service
        self._discovery_service = discovery_service
        self._service_orchestrator = service_orchestrator
    
    def scan_network(self) -> List[AddressData]:
        """Scan the configured network range."""
        network_settings = self._config_provider.get_network_settings()
        performance_settings = self._config_provider.get_performance_settings()
        
        subnet = network_settings["subnet"]
        min_ip = network_settings["min_ip"]
        max_ip = network_settings["max_ip"]
        max_threads = performance_settings["max_threads"]
        
        devices: List[AddressData] = []
        ip_range: List[str] = [f"{subnet}.{i}" for i in range(min_ip, max_ip + 1)]

        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip) for ip in ip_range]
            for future in as_completed(futures):
                device: Optional[AddressData] = future.result()
                if device is not None:
                    devices.append(device)
        return devices
    
    def scan_ip(self, ip_address: str) -> Optional[AddressData]:
        """Scan a specific IP address."""
        feature_flags = self._config_provider.get_feature_flags()
        
        # Step 1: Ping the IP
        ping_result = self._pinger.ping(ip_address)
        if not ping_result or not ping_result[0]:  # ping failed
            return None
        
        _, ping_time_ms, stdout = ping_result
        
        # Initialize data containers
        mac_address: Optional[str] = None
        arp_time_ms: int = 0
        ttl: Optional[int] = None
        open_ports: List[PortInfo] = []
        services_info: Dict[int, ServiceInfo] = {}
        
        # Step 2: ARP resolution
        if feature_flags.get("mac_resolution", False):
            arp_result = self._arp_resolver.resolve_mac_address(ip_address)
            if arp_result:
                mac_address, arp_time_ms = arp_result
        
        # Step 3: Extract TTL from ping output
        if stdout:
            ttl = self._extract_ttl_from_ping_output(stdout)
        
        # Step 4: Device enrichment (hostname, vendor, OS detection)
        enrichment_data = self._enrichment_service.enrich_device_data(
            ip_address, mac_address, ttl
        )
        
        # Step 5: Port scanning
        if feature_flags.get("port_scan", False):
            open_ports = self._port_scanner.scan_ports(ip_address, Constants.COMMON_PORTS)
        
        # Step 6: Service detection
        for port_info in open_ports:
            service_info = self._service_orchestrator.detect_service_on_port(
                ip_address, port_info.port, port_info.service or "unknown"
            )
            if service_info:
                services_info[port_info.port] = service_info
        
        # Step 7: Device discovery
        discovered_info = self._discovery_service.discover_device(ip_address)
        
        return AddressData(
            mac_address=mac_address,
            ip_address=ip_address,
            ping_time_ms=ping_time_ms,
            arp_time_ms=arp_time_ms,
            hostname=enrichment_data.get("hostname"),
            mac_vendor=enrichment_data.get("vendor"),
            os_guess=enrichment_data.get("os_guess"),
            ttl=ttl,
            open_ports=open_ports,
            services_info=services_info,
            discovered_info=discovered_info
        )
    
    def _extract_ttl_from_ping_output(self, ping_output: str) -> Optional[int]:
        """Extract TTL value from ping output."""
        try:
            ttl_match = re.search(Constants.TTL_REGEX, ping_output)
            if ttl_match:
                return int(ttl_match.group(1))
        except (ValueError, AttributeError):
            pass
        return None
    
    def get_scan_summary(self, address_data: AddressData) -> Dict[str, Any]:
        """Get a summary of scan results for display."""
        summary: Dict[str, Any] = {
            "open_ports": [],
            "services": [],
            "discovered_info": []
        }
        
        # Get open ports
        if address_data.open_ports:
            summary["open_ports"] = [f"{p.port}/{p.protocol}" for p in address_data.open_ports]
        
        # Get services
        if address_data.services_info:
            summary["services"] = [f"{port}:{service.service_name}" for port, service in address_data.services_info.items()]
        
        # Get discovery info
        if address_data.discovered_info:
            summary["discovered_info"] = [f"{d.protocol}:{d.device_type}" for d in address_data.discovered_info if d.device_type]
        
        return summary
