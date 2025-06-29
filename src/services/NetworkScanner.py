import platform
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Dict, List, Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet

import Constants
import Exceptions
from Objects.AddressData import AddressData
from Objects.DiscoveryInfo import DiscoveryInfo
from Objects.Injectable import Injectable
from Objects.PortInfo import PortInfo
from Objects.ServiceInfo import ServiceInfo
from Services.AppConfig import AppConfig
from Services.EnrichmentService import EnrichmentService
from Services.PortScannerService import PortScannerService
from Services.ServiceDetectionService import ServiceDetectionService
from Services.DiscoveryService import DiscoveryService
from Utilities.Timer import Time, time_operation


class NetworkScanner(Injectable):
    _config: AppConfig
    _enrichment_service: EnrichmentService
    _port_scanner: PortScannerService
    _service_detector: ServiceDetectionService
    
    _ping_cmd: str
    _ping_count_flag: str
    _ping_timeout_flag: str
    _ping_timeout_value: float
    
    def __init__(self, config: AppConfig, enrichment_service: EnrichmentService, port_scanner: PortScannerService, service_detector: ServiceDetectionService, discovery_service: DiscoveryService) -> None:
        self._config = config
        self._enrichment_service = enrichment_service
        self._port_scanner = port_scanner
        self._service_detector = service_detector
        self.discovery_service = discovery_service
        
        system = platform.system()
        if system not in Constants.PING_COMMANDS:
            raise Exceptions.NetworkScanError(f"Unsupported operating system: {system}")
        
        if system == Constants.PLATFORM_WINDOWS:
            self._ping_timeout_value = int(config.ping_timeout_ms)
        else:
            self._ping_timeout_value = config.ping_timeout_ms / 1000
        
        self._ping_cmd = Constants.PING_COMMANDS[system]["cmd"]
        self._ping_count_flag = Constants.PING_COMMANDS[system]["count_flag"]
        self._ping_timeout_flag = Constants.PING_COMMANDS[system]["timeout_flag"]
        
                
    def scan_network(self) -> List[AddressData]:
        devices: List[AddressData] = []
        ip_range: List[str] = [f"{self._config.subnet}.{i}" for i in range(self._config.min_ip, self._config.max_ip + 1)]

        with ThreadPoolExecutor(max_workers=self._config.max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip) for ip in ip_range]
            for future in as_completed(futures):
                device: Optional[AddressData] = future.result()
                if device is not None:
                    devices.append(device)
        return devices

    def scan_ip(self, ip_address: str) -> Optional[AddressData]:
        ping_time = Time()
        
        with time_operation(ping_time):
            try:
                result = subprocess.run(
                    [
                        self._ping_cmd,
                        self._ping_count_flag, str(self._config.ping_count),
                        self._ping_timeout_flag, str(self._ping_timeout_value),
                        ip_address
                    ],
                    capture_output=True,
                    text=True,
                    timeout=self._config.ping_timeout_ms / 1000 + 1
                )                                                      
            except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
                print(f"Ping error for {ip_address}: {e}")
                return None
                 
        if result.returncode != Constants.SUCCESSFUL_PING_EXIT_CODE:
            return None
      
        mac: Optional[str] = None
        ttl: Optional[int] = None
        arp_time: Time = Time()
        hostname: Optional[str] = None
        mac_vendor: Optional[str] = None
        os_guess: Optional[str] = None
        open_ports: List[PortInfo] = []
        services_info: Dict[int, ServiceInfo] = {}
        discovered_info: List[DiscoveryInfo] = []
      
        if self._config.mac_resolution and ip_address:
            mac, arp_time = self._lookup_arp(ip_address)
          
        if self._config.hostname_resolution and ip_address:
            hostname = self._enrichment_service.resolve_hostname(ip_address)
        
        if self._config.mac_vendor_lookup and mac:
            mac_vendor = self._enrichment_service.get_mac_vendor(mac)
            
        if self._config.os_detection and result.stdout:  
            ttl = self._extract_ttl_from_ping_output(result.stdout) 
            if ttl:
                os_guess = self._enrichment_service.guess_os_from_ttl(ttl)

        if self._config.port_scan and ip_address:
            open_ports = self._port_scanner.scan_ports(ip_address, Constants.COMMON_PORTS)

        if self._config.detect_http and open_ports:
            for port_info in open_ports:
                if port_info.port in Constants.HTTP_PORTS:
                    service_info = self._service_detector.detect_http_service(ip_address, port_info.port)
                    if service_info:
                        services_info[port_info.port] = service_info

        if self._config.detect_ssh and open_ports:
            for port_info in open_ports:
                if port_info.port == Constants.SSH_PORT:
                    service_info = self._service_detector.detect_ssh_service(ip_address, port_info.port)
                    if service_info:
                        services_info[port_info.port] = service_info
                    
        if self._config.detect_banners and open_ports:
            for port_info in open_ports:
                if port_info.service in Constants.BANNER_SERVICES:
                    service_info = self._service_detector.grab_banner(ip_address, port_info.port)
                    if service_info:
                        services_info[port_info.port] = service_info


        if self._config.discover_netbios and ip_address:
            netbios_info = self.discovery_service.discover_netbios(ip_address)
            if netbios_info:
                discovered_info.append(netbios_info)

        if self._config.discover_upnp and ip_address:
            upnp_info = self.discovery_service.discover_upnp(ip_address)
            if upnp_info:
                discovered_info.append(upnp_info)
                
        if self._config.discover_mdns and ip_address:
            mdns_info = self.discovery_service.discover_mdns(ip_address)
            if mdns_info:
                discovered_info.append(mdns_info)


        return AddressData(
            mac_address=mac, 
            ip_address=ip_address, 
            ping_time_ms=int(ping_time.value), 
            arp_time_ms=int(arp_time.value),
            hostname=hostname,
            mac_vendor=mac_vendor,
            os_guess=os_guess,
            ttl=ttl,
            open_ports=open_ports,
            services_info=services_info,
            discovered_info=discovered_info
        )

    def _lookup_arp(self, ip: str) -> Tuple[Optional[str], Time]:
        arp: Packet = ARP(pdst=ip)  # type: ignore
        ether: Packet = Ether(dst=Constants.BROADCAST_MAC_ADDRESS)  # type: ignore
        packet: Packet = ether / arp  # type: ignore

        arp_time = Time()
        with time_operation(arp_time):
            try:
                results = srp(packet, timeout=self._config.arp_timeout_ms/1000, verbose=0)[0]  # type: ignore
            except Exception as e:
                print(f"ARP lookup error for {ip}: {e}")
                return None, arp_time

        if results:
            received_pkt = results[0][1]
            mac_address = getattr(received_pkt, "hwsrc", None)
            if mac_address and isinstance(mac_address, str):
                return mac_address.lower(), arp_time
        return None, arp_time

    def _extract_ttl_from_ping_output(self, ping_output: str) -> Optional[int]:
        try:
            ttl_match = re.search(Constants.TTL_REGEX, ping_output)
            if ttl_match:
                return int(ttl_match.group(1))
        except (ValueError, AttributeError):
            pass
        return None


    def get_scan_summary(self, address_data: AddressData) -> Dict[str, Any]:
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
