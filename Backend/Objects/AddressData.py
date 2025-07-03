from dataclasses import dataclass
from typing import Dict, List, Optional

from Backend.Objects.DiscoveryInfo import DiscoveryInfo
from Backend.Objects.PortInfo import PortInfo
from Backend.Objects.ServiceInfo import ServiceInfo


@dataclass
class AddressData:
    ip_address: str
    mac_address: Optional[str]
    ping_time_ms: int
    arp_time_ms: int
    
    hostname: Optional[str] = None
    mac_vendor: Optional[str] = None
    os_guess: Optional[str] = None
    ttl: Optional[int] = None
    
    open_ports: Optional[List[PortInfo]] = None
    services_info: Optional[Dict[int, ServiceInfo]] = None  
    discovered_info: Optional[List[DiscoveryInfo]] = None

    def hasMac(self) -> bool:
        return self.mac_address is not None and len(self.mac_address) > 0

