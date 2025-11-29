from typing import Final

# HTTP
HTTP_DEFAULT_SERVER: Final[str] = "Unknown HTTP Server"
HTTP_INFO_TEMPLATE: Final[str] = "Status: {status}"
HTTP_SCHEME: Final[str] = "http"
HTTPS_SCHEME: Final[str] = "https"
HTTP_URL_TEMPLATE: Final[str] = "{protocol_scheme}://{ip_address}:{port}/"
HTTPS_PORT: Final[int] = 443
SERVER_HEADER: Final[str] = "Server"
USER_AGENT_HEADER: Final[str] = "User-Agent"
USER_AGENT_VALUE: Final[str] = "NetworkMonitor/1.0"

# SSH
SSH_DEFAULT_PRODUCT: Final[str] = "SSH Server"
SSH_BANNER_PREFIX: Final[str] = "SSH-"

# Banner / socket
MAX_BANNER_LENGTH: Final[int] = 100

# Encoding
DEFAULT_VERSION: Final[str] = "Unknown"