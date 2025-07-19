from dataclasses import dataclass


@dataclass
class ServiceInfo:
    """Information about a detected service."""
    service_name: str
    version: str | None = None
    product: str | None = None
    extra_info: str | None = None

