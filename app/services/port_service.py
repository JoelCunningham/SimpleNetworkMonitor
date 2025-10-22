import socket
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

from app import config
from app.database import Database
from app.models import Mac, Port
from app.objects import PortInfo, ServiceInfo
from app.services.interfaces import PortServiceInterface

MAX_WORKERS = 20
OPEN_PORT_RESULT = 0
UNKNOWN_PORT_TEMPLATE = "unknown-{port}"
PORT_SERVICE_MAP = {
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

class PortService(PortServiceInterface):
    """Service for handling port-related operations."""

    def __init__(self, database: Database) -> None:
        self.database = database
        self.lock = threading.Lock()

    def save_port(self, mac_record: Mac, open_ports: list[PortInfo], services_info: dict[int, ServiceInfo] | None) -> None:
        """Save port data for a MAC address."""
        if not open_ports:
            raise Exception("AddressData does not contain open ports.")

        # Remove existing port data for this MAC
        existing_ports = self.database.select_all(Port).where(Port.mac_id == mac_record.id).all()
        for port in existing_ports:
            self.database.delete(port)

        for port_info in open_ports:
            service_name = port_info.service
            banner = port_info.banner

            # Override with service detection data if available
            if services_info and port_info.port in services_info:
                service_info = services_info[port_info.port]
                if service_info.service_name:
                    service_name = service_info.service_name
                    if service_info.version:
                        service_name += f" {service_info.version}"

            port = Port(
                mac_id=mac_record.id,
                port=port_info.port,
                protocol=port_info.protocol,
                service=service_name,
                banner=banner,
            )

            self.database.create(port)
        
    def scan_ports(self, ip_address: str, ports: list[int]) -> list[PortInfo]:
        open_ports: list[PortInfo] = []
        timeout = config.port_scan_timeout_ms / 1000
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = [
                executor.submit(self._scan_port, ip_address, port, timeout)
                for port in ports
            ]
            
            for future in as_completed(futures):
                port_info = future.result()
                if port_info:
                    open_ports.append(port_info)
        
        return open_ports
    
    def _scan_port(self, ip_address: str, port: int, timeout: float) -> PortInfo | None:
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
