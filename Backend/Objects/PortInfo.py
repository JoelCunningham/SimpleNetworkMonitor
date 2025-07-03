
from dataclasses import dataclass
from typing import Optional


@dataclass
class PortInfo:
    """Information about an open port."""
    port: int
    protocol: str = "tcp"
    service: Optional[str] = None
    banner: Optional[str] = None
    state: str = "open"

