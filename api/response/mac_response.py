from datetime import datetime

from pydantic import BaseModel

from api.response.discovery_response import DiscoveryResponse
from api.response.port_response import PortResponse


class MacResponse(BaseModel):
    id: int
    address: str
    last_ip: str
    last_seen: datetime
    ping_time_ms: int | None
    arp_time_ms: int | None
    hostname: str | None
    vendor: str | None
    os_guess: str | None
    ttl: int | None
    ports: list[PortResponse] | None
    discoveries: list[DiscoveryResponse] | None