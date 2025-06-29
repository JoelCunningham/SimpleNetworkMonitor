"""Port scanning service."""
import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.INetworkScanning import IPortScanner
from Objects.Injectable import Injectable
from Objects.PortInfo import PortInfo


class PortScannerService(IPortScanner, Injectable):
    """Service responsible for port scanning operations."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
        self._lock = threading.Lock()
        self._service_map = self._build_service_map()
    
    def _build_service_map(self) -> dict[int, str]:
        """Build a mapping of common ports to service names."""
        return {
            21: "ftp",
            22: "ssh",
            23: "telnet",
            25: "smtp",
            53: "dns",
            80: "http",
            110: "pop3",
            135: "msrpc",
            139: "netbios-ssn",
            143: "imap",
            443: "https",
            993: "imaps",
            995: "pop3s",
            1723: "pptp",
            3389: "rdp",
            5900: "vnc",
            8080: "http-alt"
        }
    
    def scan_ports(self, ip_address: str, ports: List[int]) -> List[PortInfo]:
        """Scan specified ports on the given IP address."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["port_scan_timeout_ms"] / 1000.0
        
        open_ports: List[PortInfo] = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(self._scan_single_port, ip_address, port, timeout_seconds)
                for port in ports
            ]
            
            for future in as_completed(futures):
                port_info = future.result()
                if port_info:
                    open_ports.append(port_info)
        
        return open_ports
    
    def _scan_single_port(self, ip_address: str, port: int, timeout: float) -> Optional[PortInfo]:
        """Scan a single port on the target IP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((ip_address, port))
                
                if result == 0:
                    # Port is open, get service name
                    service_name = self._get_service_name(port)
                    return PortInfo(
                        port=port,
                        protocol="tcp",
                        service=service_name
                    )
        except (socket.error, OSError):
            pass
        
        return None
    
    def _get_service_name(self, port: int) -> str:
        """Get the service name for a port number."""
        try:
            # Try to get service name from system
            return socket.getservbyport(port)
        except OSError:
            # Fall back to our service map
            return self._service_map.get(port, f"unknown-{port}")
