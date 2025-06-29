import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional

from Objects.Injectable import Injectable
from Objects.PortInfo import PortInfo
from Services.AppConfig import AppConfig


class PortScannerService(Injectable):
    """Service for scanning ports and detecting services on network devices."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
    
    def scan_ports(self, ip_address: str, ports: List[int]) -> List[PortInfo]:
        """Scan specified ports on the given IP address."""        
        open_ports: List[PortInfo] = []
        
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(self._scan_single_port, ip_address, port, self._config.port_scan_timeout_ms / 1000.0)
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
                    # Port is open, try to get service name
                    service_name = self._get_service_name(port)
                    return PortInfo(
                        port=port,
                        protocol="tcp",
                        service=service_name
                    )
        except (socket.error, OSError):
            pass
        
        return None
    
    def _get_service_name(self, port: int) -> Optional[str]:
        """Get the common service name for a port number."""
        common_services = {
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
        
        try:
            # Try to get service name from system
            service_name = socket.getservbyport(port)
            return service_name
        except OSError:
            # Fall back to our common services map
            return common_services.get(port, f"unknown-{port}")
