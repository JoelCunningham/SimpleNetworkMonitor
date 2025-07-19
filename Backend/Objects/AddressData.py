from dataclasses import dataclass, field

from Backend.Objects.DiscoveryInfo import DiscoveryInfo
from Backend.Objects.PortInfo import PortInfo
from Backend.Objects.ServiceInfo import ServiceInfo


@dataclass
class AddressData:
    ip_address: str
    mac_address: str | None = None
    ping_time_ms: int | None = None
    arp_time_ms: int | None = None
    
    hostname: str | None = None
    mac_vendor: str | None = None
    os_guess: str | None = None
    ttl: int | None = None
    
    open_ports: list[PortInfo] = field(default_factory=lambda: [])
    services_info: dict[int, ServiceInfo] = field(default_factory=lambda: {})
    discovered_info: list[DiscoveryInfo] = field(default_factory=lambda: [])

    def hasMac(self) -> bool:
        return self.mac_address is not None and len(self.mac_address) > 0

