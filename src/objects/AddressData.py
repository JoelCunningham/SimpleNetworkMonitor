from dataclasses import dataclass
from typing import Optional

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

    def hasMac(self) -> bool:
        return self.mac_address is not None and len(self.mac_address) > 0