import socket
from typing import Optional, Tuple

from Backend.Constants import (CRLF, DEFAULT_ENCODING, DEFAULT_UPNP_DEVICE_TYPE,
                       ENCODING_ERROR_HANDLING, HTTP_OK_RESPONSE,
                       SOCKET_BUFFER_SIZE, SSDP_HOST_HEADER, SSDP_MAN_HEADER,
                       SSDP_MX_PREFIX, SSDP_REQUEST_LINE, SSDP_ST_HEADER,
                       ST_HEADER_PREFIX, UPNP_HEADER_SEPARATOR, UPNP_PORT,
                       UPNP_PROTOCOL_NAME, UPNP_SERVER_HEADER_PREFIX,
                       UPNP_SPLIT_LIMIT)
from Backend.Objects.DiscoveryInfo import DiscoveryInfo
from Backend.Objects.Injectable import Injectable
from Backend.Services.AppConfiguration import AppConfig


class UpnpDiscoverer(Injectable):
    """UPnP/SSDP discovery protocol implementation."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
    
    def discover(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using UPnP/SSDP."""        
        try:
            ssdp_request = (
                SSDP_REQUEST_LINE +
                SSDP_HOST_HEADER +
                SSDP_MAN_HEADER +
                SSDP_ST_HEADER +
                f"{SSDP_MX_PREFIX}{int(self._config.timeout.discovery_timeout_s())}{CRLF}" +
                CRLF
            ).encode(DEFAULT_ENCODING)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self._config.timeout.discovery_timeout_s())
            
            sock.sendto(ssdp_request, (ip_address, UPNP_PORT))
            
            try:
                response, _ = sock.recvfrom(SOCKET_BUFFER_SIZE)
                response_text = response.decode(DEFAULT_ENCODING, errors=ENCODING_ERROR_HANDLING)
                
                if HTTP_OK_RESPONSE in response_text:
                    device_name, device_type = self._parse_upnp_response(response_text)
                    if device_name or device_type:
                        return DiscoveryInfo(
                            protocol=UPNP_PROTOCOL_NAME,
                            device_name=device_name,
                            device_type= device_type or DEFAULT_UPNP_DEVICE_TYPE
                        )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None
    
    def _parse_upnp_response(self, response: str) -> Tuple[Optional[str], Optional[str]]:
        """Parse UPnP response to extract device information."""
        try:
            device_name, device_type = None, None
            lines = response.split(CRLF)
            
            for line in lines:
                if line.startswith(UPNP_SERVER_HEADER_PREFIX):
                    device_name = line.split(UPNP_HEADER_SEPARATOR, UPNP_SPLIT_LIMIT)[1].strip()
                elif line.startswith(ST_HEADER_PREFIX):
                    device_type = line.split(UPNP_HEADER_SEPARATOR, UPNP_SPLIT_LIMIT)[1].strip()
            
            return device_name, device_type
        except (IndexError, AttributeError):
            return None, None
