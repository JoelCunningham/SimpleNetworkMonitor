from typing import Final

# Common/shared constants used by multiple services
HTTP_SERVICE_NAME: Final[str] = "http"
SSH_SERVICE_NAME: Final[str] = "ssh"

DEFAULT_ENCODING: Final[str] = 'utf-8'
ENCODING_ERROR_HANDLING: Final[str] = 'ignore'
SOCKET_BUFFER_SIZE: Final[int] = 1024