from dataclasses import dataclass, field
from typing import Dict, List, Optional

from Backend.Objects.DiscoveryInfo import DiscoveryInfo
from Backend.Objects.PortInfo import PortInfo
from Backend.Objects.ServiceInfo import ServiceInfo


@dataclass
class AddressData:
    ip_address: str
    mac_address: Optional[str] = None
    ping_time_ms: Optional[int] = None
    arp_time_ms: Optional[int] = None
    
    hostname: Optional[str] = None
    mac_vendor: Optional[str] = None
    os_guess: Optional[str] = None
    ttl: Optional[int] = None
    
    open_ports: List[PortInfo] = field(default_factory=lambda: [])
    services_info: Dict[int, ServiceInfo] = field(default_factory=lambda: {})
    discovered_info: List[DiscoveryInfo] = field(default_factory=lambda: [])

    def hasMac(self) -> bool:
        return self.mac_address is not None and len(self.mac_address) > 0

