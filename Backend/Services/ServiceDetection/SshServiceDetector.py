import socket

from Backend.Constants import (DEFAULT_ENCODING, DEFAULT_SSH_PRODUCT,
                               DEFAULT_VERSION, ENCODING_ERROR_HANDLING,
                               SOCKET_BUFFER_SIZE, SSH_BANNER_PREFIX,
                               SSH_SERVICE_NAME)
from Backend.Objects.Injectable import Injectable
from Backend.Objects.ServiceInfo import ServiceInfo
from Backend.Services.AppConfiguration import AppConfig


class SshServiceDetector(Injectable):
    """Detector for SSH services."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
    
    def detect_service(self, ip_address: str, port: int) -> ServiceInfo | None:
        """Detect SSH service and get version banner."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self._config.timeout.service_detection_timeout_s())
                sock.connect((ip_address, port))
                
                banner = sock.recv(SOCKET_BUFFER_SIZE).decode(DEFAULT_ENCODING, errors=ENCODING_ERROR_HANDLING).strip()
                
                if banner.startswith(SSH_BANNER_PREFIX):
                    parts = banner.split()
                    version = parts[0] if parts else DEFAULT_VERSION
                    
                    return ServiceInfo(
                        service_name=SSH_SERVICE_NAME,
                        version=version,
                        extra_info=banner
                    )
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return ServiceInfo(service_name=SSH_SERVICE_NAME, product=DEFAULT_SSH_PRODUCT)
