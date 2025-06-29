from dataclasses import dataclass
from typing import List, Optional


@dataclass
class DiscoveryInfo:
    """Information discovered through network discovery protocols."""
    protocol: str
    device_name: Optional[str] = None
    device_type: Optional[str] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    services: Optional[List[str]] = None
    
    def __post_init__(self):
        if self.services is None:
            self.services = []
