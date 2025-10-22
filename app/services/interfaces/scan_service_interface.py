from typing import Protocol, Any


class ScanServiceInterface(Protocol):
    """Interface for network scanning operations."""

    def scan_network(self, scan_options: Any) -> list[Any]:
        ...

    def scan_ip(self, ip_address: str, scan_options: Any) -> Any:
        ...

    def save_mac_scan(self, address_data: Any) -> None:
        ...

    def save_full_scan(self, address_data: Any) -> None:
        ...
