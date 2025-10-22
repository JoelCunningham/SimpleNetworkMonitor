from typing import Protocol, Any


class PortServiceInterface(Protocol):
    """Interface for port scanning and storage."""

    def scan_ports(self, ip_address: str, ports: list[int]) -> list[Any]:
        ...

    def save_port(self, mac_record: Any, open_ports: list[Any], services_info: dict[Any, Any]) -> None:
        ...
