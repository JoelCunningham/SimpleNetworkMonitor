import socket

from Backend.Objects.Injectable import Injectable
from Backend.Services.AppConfiguration import AppConfig


class HostnameResolver(Injectable):
    """Service responsible for hostname resolution."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
    
    def resolve_hostname(self, ip_address: str) -> str | None:
        """Resolve hostname from IP address."""
        try:
            socket.setdefaulttimeout(self._config.timeout.hostname_timeout_s())
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname
        except (socket.herror, socket.gaierror, socket.timeout):
            return None
        finally:
            socket.setdefaulttimeout(None)