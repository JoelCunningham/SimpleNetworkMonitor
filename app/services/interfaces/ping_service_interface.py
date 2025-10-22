from typing import Protocol


class PingServiceInterface(Protocol):
    """Interface for ping/ICMP related operations."""

    def ping(self, ip_address: str) -> tuple[bool | None, int, str | None]:
        ...

    def get_hostname(self, ip_address: str) -> str | None:
        ...

    def get_ttl_from_ping(self, ping_result: str) -> int | None:
        ...

    def get_os_from_ttl(self, ttl: int) -> str | None:
        ...
