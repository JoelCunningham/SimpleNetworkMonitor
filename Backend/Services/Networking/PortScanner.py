import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from Backend.Constants import (MAX_WORKERS, OPEN_PORT_RESULT, PORT_SERVICE_MAP,
                       UNKNOWN_PORT_TEMPLATE)
from Backend.Objects.Injectable import Injectable
from Backend.Objects.PortInfo import PortInfo
from Backend.Services.AppConfiguration import AppConfig


class PortScanner(Injectable):
    """Port scanning service."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
    
    def scan_ports(self, ip_address: str, ports: list[int]) -> list[PortInfo]:
        """Scan specified ports on the given IP address."""        
        open_ports: list[PortInfo] = []
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(self._scan_single_port, ip_address, port, self._config.timeout.port_scan_timeout_s())
                for port in ports
            ]
            
            for future in as_completed(futures):
                port_info = future.result()
                if port_info:
                    open_ports.append(port_info)
        
        return open_ports
    
    def _scan_single_port(self, ip_address: str, port: int, timeout: float) -> PortInfo | None:
        """Scan a single port on the target IP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((ip_address, port))
                
                if result == OPEN_PORT_RESULT:
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
            return socket.getservbyport(port)
        except OSError:
            return PORT_SERVICE_MAP.get(port, UNKNOWN_PORT_TEMPLATE.format(port=port))
