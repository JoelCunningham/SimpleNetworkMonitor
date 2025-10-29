from typing import Protocol

from app.common.objects.service_info import ServiceInfo


class ProtocolServiceInterface(Protocol):
    """Interface for protocol/service detection (HTTP, SSH, banners)."""

    def detect_http(self, ip: str, port: int) -> ServiceInfo | None:
        """Detect HTTP service information (server header, status)."""
        ...

    def detect_ssh(self, ip: str, port: int) -> ServiceInfo | None:
        """Detect SSH service (banner/version)."""
        ...

    def detect_banner(self, ip: str, port: int, service_name: str) -> ServiceInfo | None:
        """Generic banner detection for text-based services."""
        ...
