from dataclasses import dataclass
from typing import Optional

@dataclass
class AddressData:
    ip: str
    mac: Optional[str]
    ping_time_ms: int
    arp_time_ms: int

    def hasMac(self) -> bool:
        return self.mac is not None and len(self.mac) > 0