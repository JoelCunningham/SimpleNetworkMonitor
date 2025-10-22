from typing import Protocol, Any


class DiscoveryServiceInterface(Protocol):
    """Interface for discovery helpers (NetBIOS, UPnP, mDNS)."""

    def discover_netbios(self, ip: str) -> Any | None:
        ...

    def discover_upnp(self, ip: str) -> Any | None:
        ...

    def discover_mdns(self, ip: str) -> Any | None:
        ...
