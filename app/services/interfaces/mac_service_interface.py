from typing import Protocol

from app.models import Mac
from app.objects import AddressData


class MacServiceInterface(Protocol):
    """Interface for MAC/ARP resolution and storage."""

    def save_mac(self, address_data: AddressData, preserve: bool = False) -> Mac:
        """Save or update MAC address data."""
        ...
        
    def get_mac_by_address(self, mac_address: str) -> Mac | None:
        """Get MAC address by address string."""
        ...
        
    def resolve_mac_address(self, ip_address: str) -> tuple[str, int] | None:
        """Resolve MAC address for IP."""   
        ...
        
    def get_vendor_from_mac(self, mac_address: str) -> str | None:
        """Get vendor name from MAC address using OUI lookup."""
        ...
