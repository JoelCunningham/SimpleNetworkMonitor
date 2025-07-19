from dataclasses import dataclass


@dataclass
class DiscoveryInfo:
    """Information discovered through network discovery protocols."""
    protocol: str
    device_name: str | None = None
    device_type: str | None = None
    manufacturer: str | None = None
    model: str | None = None
    services: list[str] | None = None
    
    def __post_init__(self):
        if self.services is None:
            self.services = []
