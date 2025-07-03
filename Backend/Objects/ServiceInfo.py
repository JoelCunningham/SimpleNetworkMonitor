from dataclasses import dataclass
from typing import Optional


@dataclass
class ServiceInfo:
    """Information about a detected service."""
    service_name: str
    version: Optional[str] = None
    product: Optional[str] = None
    extra_info: Optional[str] = None

