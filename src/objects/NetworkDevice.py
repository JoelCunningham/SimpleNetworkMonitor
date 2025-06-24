from dataclasses import dataclass

@dataclass
class NetworkDevice:
    ip: str
    mac: str
    name: str
    ping_time_ms: float
    arp_time_ms: float