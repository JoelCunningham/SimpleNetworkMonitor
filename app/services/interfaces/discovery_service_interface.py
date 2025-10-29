from typing import Protocol

from app.database.models import Mac
from app.objects import DiscoveryInfo


class DiscoveryServiceInterface(Protocol):
    """Interface for discovery helpers (NetBIOS, UPnP, mDNS)."""

    def save_discoveries(self, mac: Mac, discoveries: list[DiscoveryInfo]) -> None:
        """Save discovery information to the database."""
        ...

    def discover_mdns(self, ip_address: str) -> DiscoveryInfo | None:
        """Discover device information using mDNS/Bonjour."""
        ...
        
    def discover_netbios(self, ip_address: str) -> DiscoveryInfo | None:
        """Discover device information using NetBIOS name service."""
        ...

    def discover_upnp(self, ip_address: str) -> DiscoveryInfo | None:
        """Discover device information using UPnP/SSDP."""
        ...
