from typing import Final

# Scan service constants
BANNER_SERVICE_NAMES: Final[list[str]] = ["telnet", "smtp", "pop3", "imap", "ftp"]
COMMON_PORTS: Final[list[int]] = [21, 22, 23, 25, 53, 80, 110, 135, 139, 143, 443, 993, 995, 1723, 3389, 5900, 8080]
HTTP_PORTS: Final[list[int]] = [80, 443, 8080, 8443]
SSH_PORT: Final[int] = 22
MAX_MESSAGE_LENGTH: Final[int] = 80