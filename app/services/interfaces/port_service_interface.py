from typing import Protocol

from app.database.models import Mac
from app.common.objects import PortInfo, ServiceInfo


class PortServiceInterface(Protocol):
    """Interface for port scanning and storage."""

    def scan_ports(self, ip_address: str, ports: list[int]) -> list[PortInfo]:
        """Scan specified ports on an IP address and return open PortInfo entries."""
        ...

    def save_port(self, mac_record: Mac, open_ports: list[PortInfo], services_info: dict[int, ServiceInfo] | None) -> None:
        """Persist open port information for a MAC address."""
        ...
