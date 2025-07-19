import socket
import struct

from Backend.Constants import (ASCII_ENCODING, ENCODING_ERROR_HANDLING,
                       NETBIOS_ADDITIONAL_COUNT, NETBIOS_ANSWERS_COUNT,
                       NETBIOS_AUTHORITY_COUNT, NETBIOS_HEADER_LENGTH,
                       NETBIOS_MAX_NAME_LENGTH, NETBIOS_MIN_RESPONSE_LENGTH,
                       NETBIOS_MIN_WORD_LENGTH, NETBIOS_NAME_LENGTH,
                       NETBIOS_PORT, NETBIOS_PROTOCOL_NAME,
                       NETBIOS_QUERY_FLAGS, NETBIOS_QUERY_SUFFIX,
                       NETBIOS_QUESTIONS_COUNT, NETBIOS_TRANSACTION_ID,
                       NETBIOS_WILDCARD, SOCKET_BUFFER_SIZE,
                       STRUCT_PACK_FORMAT, WINDOWS_DEVICE_TYPE)
from Backend.Objects.DiscoveryInfo import DiscoveryInfo
from Backend.Objects.Injectable import Injectable
from Backend.Services.AppConfiguration import AppConfig


class NetBiosDiscoverer(Injectable):
    """NetBIOS discovery protocol implementation."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config

    def discover(self, ip_address: str) -> DiscoveryInfo | None:
        """Discover device information using NetBIOS Name Service."""      
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self._config.timeout.discovery_timeout_s())
            
            query_packet = struct.pack(
                STRUCT_PACK_FORMAT, 
                NETBIOS_TRANSACTION_ID, 
                NETBIOS_QUERY_FLAGS,        
                NETBIOS_QUESTIONS_COUNT,             
                NETBIOS_ANSWERS_COUNT,            
                NETBIOS_AUTHORITY_COUNT,            
                NETBIOS_ADDITIONAL_COUNT        
            )
            
            name_query = NETBIOS_NAME_LENGTH + NETBIOS_WILDCARD + NETBIOS_QUERY_SUFFIX
            query_packet += name_query
            
            sock.sendto(query_packet, (ip_address, NETBIOS_PORT))
            
            try:
                response, _ = sock.recvfrom(SOCKET_BUFFER_SIZE)
                
                if len(response) > NETBIOS_HEADER_LENGTH:
                    device_name = self._parse_netbios_response(response)
                    if device_name:
                        return DiscoveryInfo(
                            protocol=NETBIOS_PROTOCOL_NAME,
                            device_name=device_name,
                            device_type=WINDOWS_DEVICE_TYPE
                        )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, struct.error):
            pass
        
        return None
    
    def _parse_netbios_response(self, response: bytes) -> str | None:
        """Parse NetBIOS response to extract device name."""
        try:
            if len(response) > NETBIOS_MIN_RESPONSE_LENGTH:
                decoded = response[NETBIOS_HEADER_LENGTH:].decode(ASCII_ENCODING, errors=ENCODING_ERROR_HANDLING)
                words = decoded.split()
                for word in words:
                    if len(word) > NETBIOS_MIN_WORD_LENGTH and word.isalnum():
                        return word[:NETBIOS_MAX_NAME_LENGTH]
        except (UnicodeDecodeError, IndexError):
            pass
        
        return None
