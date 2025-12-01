import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from app import config
from app.common.constants import *
from app.common.objects import PortInfo, ServiceInfo
from app.database.interfaces import DatabaseInterface
from app.database.models import Mac, Port
from app.services.interfaces import PortServiceInterface


class PortService(PortServiceInterface):
    """Service for handling port-related operations."""

    def __init__(self, database: DatabaseInterface) -> None:
        self.database = database
        self.lock = threading.Lock()

    def save_port(self, mac_record: Mac, open_ports: list[PortInfo], services_info: dict[int, ServiceInfo] | None) -> None:
        """Save port data for a MAC address."""
        if not open_ports:
            raise Exception("AddressData does not contain open ports.")

        # Remove existing port data for this MAC
        existing_ports = self.database.select(Port).where(Port.mac_id == mac_record.id).all()
        for port in existing_ports:
            self.database.hard_delete(port)

        for port_info in open_ports:
            service_name = port_info.service
            banner = port_info.banner

            # Override with service detection data if available
            if services_info and port_info.number in services_info:
                service_info = services_info[port_info.number]
                if service_info.service_name:
                    service_name = service_info.service_name
                    if service_info.version:
                        service_name += f" {service_info.version}"

            port = Port(
                mac_id=mac_record.id,
                number=port_info.number,
                protocol=port_info.protocol,
                service=service_name,
                banner=banner,
            )

            self.database.create(port)
        
    def scan_ports(self, ip_address: str, ports: list[int], udp_ports: list[int]) -> list[PortInfo]:
        """Scan TCP and optionally UDP ports on target IP."""
        open_ports: list[PortInfo] = []
        timeout = config.port_scan_timeout_ms / 1000
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(self._scan_tcp_port, ip_address, port, timeout)
                for port in ports
            ]
            
            for future in as_completed(futures):
                port_info = future.result()
                if port_info:
                    open_ports.append(port_info)
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(self._scan_udp_port, ip_address, port, timeout)
                for port in udp_ports
            ]
            
            for future in as_completed(futures):
                port_info = future.result()
                if port_info:
                    open_ports.append(port_info)
        
        return open_ports
    
    def _scan_tcp_port(self, ip_address: str, port: int, timeout: float) -> PortInfo | None:
        """Scan a single TCP port on the target IP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                adaptive_timeout = timeout if port < 1024 else timeout * 1.5
                sock.settimeout(adaptive_timeout)
                result = sock.connect_ex((ip_address, port))
                
                if result == OPEN_PORT_RESULT:
                    return PortInfo(
                        number=port,
                        protocol=TCP_PROTOCOL,
                        service=self._get_service_name(port, protocol=TCP_PROTOCOL)
                    )
        except (socket.error, OSError):
            pass
        
        return None
    
    def _scan_udp_port(self, ip_address: str, port: int, timeout: float) -> PortInfo | None:
        """Scan a single UDP port on the target IP."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
                sock.settimeout(timeout)
                
                sock.sendto(b'', (ip_address, port))
                
                try:
                    data, _ = sock.recvfrom(1024)
                    if data:
                        return PortInfo(
                            number=port,
                            protocol=UDP_PROTOCOL,
                            service=self._get_service_name(port, protocol=UDP_PROTOCOL)
                        )
                except socket.timeout:
                    if port in UDP_COMMON_PORTS:
                        return PortInfo(
                            number=port,
                            protocol=UDP_PROTOCOL,
                            service= self._get_service_name(port, protocol=UDP_PROTOCOL)
                        )
        except (socket.error, OSError):
            pass
        
        return None
    
    def _get_service_name(self, port: int, protocol: str) -> str:
        """Get the service name for a port number."""
        try:
            return socket.getservbyport(port, protocol)
        except OSError:
            return UNKNOWN_PORT_NAME
