
from dataclasses import dataclass


@dataclass
class PortInfo:
    """Information about an open port."""
    port: int
    protocol: str = "tcp"
    service: str | None = None
    banner: str | None = None
    state: str = "open"

