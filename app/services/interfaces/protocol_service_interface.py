from typing import Protocol, Any


class ProtocolServiceInterface(Protocol):
    """Interface for protocol/service detection (HTTP, SSH, banners)."""

    def detect_http(self, ip: str, port: int) -> Any | None:
        ...

    def detect_ssh(self, ip: str, port: int) -> Any | None:
        ...

    def detect_banner(self, ip: str, port: int, service_name: str) -> Any | None:
        ...
