import socket
import struct
from typing import Optional

from Constants import (DEVICE_INFO_SERVICE_TYPE, HTTP_SERVICE_TYPE,
                       IP_SEPARATOR, LAST_OCTET_INDEX, MDNS_ADDITIONAL_COUNT,
                       MDNS_ANSWERS_COUNT, MDNS_AUTHORITY_COUNT,
                       MDNS_DEVICE_NAME_PREFIX, MDNS_DEVICE_TYPE, MDNS_FLAGS,
                       MDNS_HEADER_LENGTH, MDNS_PORT, MDNS_PROTOCOL_NAME,
                       MDNS_QUESTIONS_COUNT, MDNS_SERVICE_QUERY,
                       MDNS_TRANSACTION_ID, SOCKET_BUFFER_SIZE,
                       STRUCT_PACK_FORMAT)
from Objects.DiscoveryInfo import DiscoveryInfo
from Objects.Injectable import Injectable
from Services.AppConfiguration import AppConfig


class MdnsDiscoverer(Injectable):
    """mDNS/Bonjour discovery protocol implementation."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        
    def discover(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using mDNS."""      
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self._config.timeout.discovery_timeout_s())
            
            query_packet = struct.pack(STRUCT_PACK_FORMAT, 
                MDNS_TRANSACTION_ID, 
                MDNS_FLAGS, 
                MDNS_QUESTIONS_COUNT,     
                MDNS_ANSWERS_COUNT,      
                MDNS_AUTHORITY_COUNT,      
                MDNS_ADDITIONAL_COUNT      
            )
            
            service_query = MDNS_SERVICE_QUERY
            query_packet += service_query
            
            sock.sendto(query_packet, (ip_address, MDNS_PORT))
            
            try:
                response, _ = sock.recvfrom(SOCKET_BUFFER_SIZE)
                
                if len(response) > MDNS_HEADER_LENGTH:
                    if HTTP_SERVICE_TYPE in response or DEVICE_INFO_SERVICE_TYPE in response:
                        return DiscoveryInfo(
                            protocol=MDNS_PROTOCOL_NAME,
                            device_name=f"{MDNS_DEVICE_NAME_PREFIX}{ip_address.split(IP_SEPARATOR)[LAST_OCTET_INDEX]}",
                            device_type=MDNS_DEVICE_TYPE
                        )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, struct.error):
            pass
        
        return None
