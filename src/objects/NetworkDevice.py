from dataclasses import dataclass
from typing import Optional

from objects.KnownDevice import KnownDevice


@dataclass
class NetworkDevice:
    ip: str
    mac: Optional[str]
    ping_time_ms: float
    arp_time_ms: float
    
    resolved: Optional[KnownDevice]    