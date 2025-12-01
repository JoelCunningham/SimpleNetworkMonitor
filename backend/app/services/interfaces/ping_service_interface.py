from typing import Protocol


class PingServiceInterface(Protocol):
    """Interface for ping related operations."""

    def ping(self, ip_address: str) -> tuple[int, str] | None:
        """Ping an IP address and return (success, rtt_ms, stdout_if_success_else_None)."""
        ...

    def get_hostname(self, ip_address: str) -> str | None:
        """Resolve hostname for an IP or return None."""
        ...

    def get_ttl_from_ping(self, ping_result: str) -> int | None:
        """Extract TTL from a ping output string."""
        ...

    def get_os_from_ttl(self, ttl: int) -> str:
        """Map a TTL value to a human-friendly OS string (always returns a string)."""
        ...
