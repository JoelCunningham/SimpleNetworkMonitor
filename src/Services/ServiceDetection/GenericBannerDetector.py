import socket
from typing import Optional

from Constants import (DEFAULT_ENCODING, ENCODING_ERROR_HANDLING,
                       MAX_BANNER_LENGTH, SOCKET_BUFFER_SIZE)
from Objects.Injectable import Injectable
from Services.AppConfiguration import AppConfig


class GenericBannerDetector(Injectable):
    """Generic banner grabbing service."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
    
    def grab_banner(self, ip_address: str, port: int) -> Optional[str]:
        """Generic banner grabbing for text-based services."""        
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self._config.timeout.service_detection_timeout_s())
                sock.connect((ip_address, port))
                
                banner = sock.recv(SOCKET_BUFFER_SIZE).decode(DEFAULT_ENCODING, errors=ENCODING_ERROR_HANDLING).strip()
                
                if banner:
                    return banner[:MAX_BANNER_LENGTH]
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None
