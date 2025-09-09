import socket
import struct

from app import config, database
from app.models.discovery import Discovery
from app.models.mac import Mac
from app.objects.discovery_info import DiscoveryInfo

MDNS_ADDITIONAL_COUNT = 0
MDNS_ANSWERS_COUNT = 0
MDNS_AUTHORITY_COUNT = 0
MDNS_DEVICE_NAME_PREFIX = "mDNS-"
MDNS_DEVICE_TYPE = "mDNS/Bonjour Device"
MDNS_FLAGS = 0x0000
MDNS_HEADER_LENGTH = 12
MDNS_PORT = 5353
MDNS_PROTOCOL_NAME = "mdns"
MDNS_QUESTIONS_COUNT = 1
MDNS_SERVICE_QUERY = b'\x09_services\x07_dns-sd\x04_udp\x05local\x00\x00\x0c\x00\x01'
MDNS_TRANSACTION_ID = 0x0000

NETBIOS_ADDITIONAL_COUNT = 0
NETBIOS_ANSWERS_COUNT = 0
NETBIOS_AUTHORITY_COUNT = 0
NETBIOS_HEADER_LENGTH = 12
NETBIOS_MAX_NAME_LENGTH = 15
NETBIOS_MIN_RESPONSE_LENGTH = 50
NETBIOS_MIN_WORD_LENGTH = 2
NETBIOS_NAME_LENGTH = b'\x20'
NETBIOS_PORT = 137
NETBIOS_PROTOCOL_NAME = "netbios"
NETBIOS_QUERY_FLAGS = 0x0110
NETBIOS_QUERY_SUFFIX = b'\x00\x00\x20\x00\x01'
NETBIOS_QUESTIONS_COUNT = 1
NETBIOS_TRANSACTION_ID = 0x1234
NETBIOS_WILDCARD = b'A' * 31

UPNP_DEVICE_TYPE = "UPnP Device"
SSDP_HOST_HEADER = "HOST: 239.255.255.250:1900\r\n"
SSDP_MAN_HEADER = 'MAN: "ssdp:discover"\r\n'
SSDP_MX_PREFIX = "MX: "
SSDP_REQUEST_LINE = "M-SEARCH * HTTP/1.1\r\n"
SSDP_ST_HEADER = "ST: upnp:rootdevice\r\n"
UPNP_HEADER_SEPARATOR = ':'
UPNP_PORT = 1900
UPNP_PROTOCOL_NAME = "upnp"
UPNP_SERVER_HEADER_PREFIX = 'SERVER:'
UPNP_SPLIT_LIMIT = 1

DEVICE_INFO_SERVICE_TYPE = b'_device-info._tcp'
HTTP_SERVICE_TYPE = b'_http._tcp'
IP_SEPARATOR = '.'
LAST_OCTET_INDEX = -1
ASCII_ENCODING = 'ascii'
WINDOWS_DEVICE_TYPE = "Windows/SMB Device"
HTTP_OK_RESPONSE = "HTTP/1.1 200 OK"
ST_HEADER_PREFIX = 'ST:'

CRLF = "\r\n"
DEFAULT_ENCODING = 'utf-8'
ENCODING_ERROR_HANDLING = 'ignore'
SOCKET_BUFFER_SIZE = 1024
STRUCT_PACK_FORMAT = '>HHHHHH'

class DiscoveryService():
    """Service for managing network discovery operations."""
    
    def save_discoveries(self, mac: Mac, discoveries: list[DiscoveryInfo]) -> None:
        """Save discovery data for a MAC address."""
        if not discoveries:
            raise Exception("AddressData does not contain discovery information.")

        # Remove existing discovery data for this MAC
        existing_discoveries = database.select_all(Discovery).where(Discovery.mac_id == mac.id).all()
        for discovery in existing_discoveries:
            database.delete(discovery)
        
        # Add new discovery data
        for discovery_info in discoveries:
            discovery = Discovery(
                mac_id=mac.id,
                protocol=discovery_info.protocol,
                device_name=discovery_info.device_name,
                device_type=discovery_info.device_type,
                manufacturer=discovery_info.manufacturer,
                model=discovery_info.model
            )
            database.save(discovery)

    def discover_mdns(self, ip_address: str) -> DiscoveryInfo | None:
        """Discover device information using mDNS."""      
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
                device_name = self.parse_mdns_response(response, ip_address)
                
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
        """Discover device information using NetBIOS Name Service."""      
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
        """Discover device information using UPnP/SSDP."""        
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
    
    def parse_mdns_response(self, response: bytes, ip_address: str) -> str | None:
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
