from datetime import datetime
from typing import Protocol

from app.common.objects import AddressData, ScanOptions


class ScanServiceInterface(Protocol):
    """Interface for network scanning operations."""

    def get_latest_scan_date(self) -> datetime | None:
        """Return the last_seen of the most recently observed MAC."""
        ...

    def scan_network(self, scan_options: ScanOptions) -> list[AddressData]:
        ...

    def scan_ip(self, ip_address: str, scan_options: ScanOptions) -> AddressData | None:
        ...

    def save_mac_scan(self, address_data: AddressData) -> None:
        ...

    def save_full_scan(self, address_data: AddressData) -> None:
        ...
