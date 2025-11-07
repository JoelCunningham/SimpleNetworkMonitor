import socket
import struct

from app import config
from app.common.constants import *
from app.common.objects import DiscoveryInfo
from app.database.interfaces import DatabaseInterface
from app.database.models import Discovery, Mac
from app.services.interfaces import DiscoveryServiceInterface


class DiscoveryService(DiscoveryServiceInterface):
    """Service for managing network discovery operations."""

    def __init__(self, database: DatabaseInterface) -> None:
        self.database = database

    def save_discoveries(self, mac: Mac, discoveries: list[DiscoveryInfo]) -> None:
        """Save discovery data for a MAC address."""
        if not discoveries:
            raise Exception("AddressData does not contain discovery information.")

        # Remove existing discovery data for this MAC
        existing_discoveries = self.database.select(Discovery).where(Discovery.mac_id == mac.id).all()
        for discovery in existing_discoveries:
            self.database.delete(discovery)

        # Add new discovery data
        for discovery_info in discoveries:
            discovery = Discovery(
                mac_id=mac.id,
                protocol=discovery_info.protocol,
                device_name=discovery_info.device_name,
                device_type=discovery_info.device_type,
                manufacturer=discovery_info.manufacturer,
                model=discovery_info.model,
            )
            self.database.create(discovery)

    def discover_mdns(self, ip_address: str) -> DiscoveryInfo | None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(config.discovery_timeout_ms / 1000)
            
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
                device_name = self._parse_mdns_response(response, ip_address)
                
                if device_name:
                    return DiscoveryInfo(
                        protocol=MDNS_PROTOCOL_NAME,
                        device_name=device_name,
                        device_type=MDNS_DEVICE_TYPE
                    )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, struct.error):
            pass
        
        return None

    def discover_netbios(self, ip_address: str) -> DiscoveryInfo | None:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(config.discovery_timeout_ms / 1000)
            
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
    
    def discover_upnp(self, ip_address: str) -> DiscoveryInfo | None:
        try:
            timeout = config.discovery_timeout_ms / 1000    
                        
            ssdp_request = (
                SSDP_REQUEST_LINE +
                SSDP_HOST_HEADER +
                SSDP_MAN_HEADER +
                SSDP_ST_HEADER +
                f"{SSDP_MX_PREFIX}{int(timeout)}{CRLF}" +
                CRLF
            ).encode(DEFAULT_ENCODING)
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout)
            
            sock.sendto(ssdp_request, (ip_address, UPNP_PORT))
            
            try:
                response, _ = sock.recvfrom(SOCKET_BUFFER_SIZE)
                device_name, device_type = self._parse_upnp_response(response)
                
                if device_name or device_type:
                    return DiscoveryInfo(
                        protocol=UPNP_PROTOCOL_NAME,
                        device_name=device_name,
                        device_type= device_type or UPNP_DEVICE_TYPE
                    )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None
    
    def _parse_mdns_response(self, response: bytes, ip_address: str) -> str | None:
        """Parse mDNS response to extract device information."""
        try:
            if len(response) > MDNS_HEADER_LENGTH:
                if HTTP_SERVICE_TYPE in response or DEVICE_INFO_SERVICE_TYPE in response:
                    return f"{MDNS_DEVICE_NAME_PREFIX}{ip_address.split(IP_SEPARATOR)[LAST_OCTET_INDEX]}"
        except (UnicodeDecodeError, IndexError):
            pass
        
        return None
    
    def _parse_netbios_response(self, response: bytes) -> str | None:
        """Parse NetBIOS response to extract device name."""
        try:
            if len(response) > NETBIOS_HEADER_LENGTH:
                if len(response) > NETBIOS_MIN_RESPONSE_LENGTH:
                    decoded = response[NETBIOS_HEADER_LENGTH:].decode(ASCII_ENCODING, errors=ENCODING_ERROR_HANDLING)
                    words = decoded.split()
                    for word in words:
                        if len(word) > NETBIOS_MIN_WORD_LENGTH and word.isalnum():
                            return word[:NETBIOS_MAX_NAME_LENGTH]
        except (UnicodeDecodeError, IndexError):
            pass
        
        return None
    
    def _parse_upnp_response(self, response: bytes) -> tuple[str | None, str | None]:
        """Parse UPnP response to extract device information."""
        try:
            device_name, device_type = None, None
            response_text = response.decode(DEFAULT_ENCODING, errors=ENCODING_ERROR_HANDLING)
            
            if HTTP_OK_RESPONSE in response_text:
                lines = response_text.split(CRLF)
                
                for line in lines:
                    if line.startswith(UPNP_SERVER_HEADER_PREFIX):
                        device_name = line.split(UPNP_HEADER_SEPARATOR, UPNP_SPLIT_LIMIT)[1].strip()
                    elif line.startswith(ST_HEADER_PREFIX):
                        device_type = line.split(UPNP_HEADER_SEPARATOR, UPNP_SPLIT_LIMIT)[1].strip()
                
                return device_name, device_type
            return None, None
        except (IndexError, AttributeError):
            return None, None
