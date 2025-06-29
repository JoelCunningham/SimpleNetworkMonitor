import socket
import struct
from typing import List, Dict, Optional, Any

from Objects.DiscoveryInfo import DiscoveryInfo
from Objects.Injectable import Injectable
from Services.AppConfig import AppConfig

class DiscoveryService(Injectable):
    """Service for discovering devices using various network discovery protocols."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._discovery_cache: Dict[str, List[DiscoveryInfo]] = {}
    
    def discover_netbios(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using NetBIOS Name Service."""
        try:
            # NetBIOS Name Service query (port 137/udp)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self._config.discovery_timeout_ms / 1000)
            
            # NetBIOS name query packet for wildcard query
            transaction_id = 0x1234
            query_packet = struct.pack('>HHHHHH', 
                transaction_id,  # Transaction ID
                0x0110,         # Flags: Standard query, recursion desired
                1,              # Questions
                0,              # Answer RRs
                0,              # Authority RRs
                0               # Additional RRs
            )
            
            # Query for "*" (wildcard) - encoded as 32 'A's in NetBIOS format
            name_query = b'\x20' + b'A' * 31 + b'\x00\x00\x20\x00\x01'
            query_packet += name_query
            
            sock.sendto(query_packet, (ip_address, 137))
            
            try:
                response, _ = sock.recvfrom(1024)
                sock.close()
                
                if len(response) > 12:
                    # Try to extract NetBIOS name from response
                    # This is a simplified parser - NetBIOS responses are complex
                    device_name = self._parse_netbios_response(response)
                    if device_name:
                        return DiscoveryInfo(
                            protocol="netbios",
                            device_name=device_name,
                            device_type="Windows/SMB Device"
                        )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, struct.error):
            pass
        
        return None
    
    def _parse_netbios_response(self, response: bytes) -> Optional[str]:
        """Parse NetBIOS response to extract device name."""
        try:
            # Skip header (12 bytes) and look for name in response
            if len(response) > 50:
                # Look for readable ASCII strings that might be computer names
                decoded = response[12:].decode('ascii', errors='ignore')
                # Extract first word that looks like a computer name
                words = decoded.split()
                for word in words:
                    if len(word) > 2 and word.isalnum():
                        return word[:15]  # NetBIOS names are max 15 chars
        except (UnicodeDecodeError, IndexError):
            pass
        
        return None
    
    def discover_upnp(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using UPnP/SSDP."""
        try:
            # Send SSDP M-SEARCH request
            ssdp_request = (
                "M-SEARCH * HTTP/1.1\r\n"
                "HOST: 239.255.255.250:1900\r\n"
                "MAN: \"ssdp:discover\"\r\n"
                "ST: upnp:rootdevice\r\n"
                f"MX: {int(self._config.discovery_timeout_ms / 1000)}\r\n"
                "\r\n"
            ).encode('utf-8')
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self._config.discovery_timeout_ms / 1000)
            
            # Send to specific IP instead of multicast for targeted discovery
            sock.sendto(ssdp_request, (ip_address, 1900))
            
            try:
                response, _ = sock.recvfrom(2048)
                response_str = response.decode('utf-8', errors='ignore')
                
                # Parse SSDP response
                device_info = self._parse_ssdp_response(response_str)
                if device_info:
                    return DiscoveryInfo(
                        protocol="upnp",
                        device_name=device_info.get("device_name"),
                        device_type=device_info.get("device_type"),
                        manufacturer=device_info.get("manufacturer"),
                        model=device_info.get("model"),
                        services=device_info.get("services", [])
                    )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None
    
    def _parse_ssdp_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse SSDP response headers."""
        try:
            lines = response.split('\r\n')
            headers = {}
            
            for line in lines[1:]:  # Skip first line (HTTP status)
                if ':' in line:
                    key, value = line.split(':', 1)
                    headers[key.strip().upper()] = value.strip()
            
            # Extract useful information
            device_info: Dict[str, Any] = {}
            
            if 'SERVER' in headers:
                server = headers['SERVER'] # type: ignore
                device_info["device_name"] = server
                
                # Try to extract device type and manufacturer from server string
                if 'Windows' in server:
                    device_info["device_type"] = "Windows Media Device"
                elif 'Linux' in server:
                    device_info["device_type"] = "Linux UPnP Device"
                elif 'Router' in server.lower(): # type: ignore
                    device_info["device_type"] = "Router"
            
            if 'LOCATION' in headers:
                # Could fetch device description from location URL
                device_info["services"] = ["UPnP"]
            
            return device_info if device_info else None
        
        except (ValueError, IndexError):
            pass
        
        return None
    
    def discover_mdns(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using mDNS (Multicast DNS)."""
        try:
            # mDNS query for _services._dns-sd._udp.local
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(self._config.discovery_timeout_ms / 1000)
            
            # Build mDNS query packet
            transaction_id = 0x0000
            query_packet = struct.pack('>HHHHHH',
                transaction_id,  # Transaction ID
                0x0000,         # Flags: Standard query
                1,              # Questions
                0,              # Answer RRs
                0,              # Authority RRs
                0               # Additional RRs
            )
            
            # Query for _services._dns-sd._udp.local (service discovery)
            services_query = self._encode_dns_name("_services._dns-sd._udp.local")
            services_query += struct.pack('>HH', 12, 1)  # PTR query, IN class
            
            query_packet += services_query
            
            sock.sendto(query_packet, (ip_address, 5353))
            
            try:
                response, _ = sock.recvfrom(2048)
                
                # Parse mDNS response
                device_info = self._parse_mdns_response(response)
                if device_info:
                    return DiscoveryInfo(
                        protocol="mdns",
                        device_name=device_info.get("device_name"),
                        device_type=device_info.get("device_type", "mDNS Device"),
                        services=device_info.get("services", [])
                    )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, struct.error):
            pass
        
        return None
    
    def _encode_dns_name(self, name: str) -> bytes:
        """Encode a DNS name for use in DNS packets."""
        encoded = b''
        for part in name.split('.'):
            if part:
                encoded += struct.pack('B', len(part)) + part.encode('utf-8')
        encoded += b'\x00'  # Null terminator
        return encoded
    
    def _parse_mdns_response(self, response: bytes) -> Optional[Dict[str, Any]]:
        """Parse mDNS response to extract device information."""
        try:
            if len(response) < 12:
                return None
            
            # Parse header
            header = struct.unpack('>HHHHHH', response[:12])
            answer_count = header[2]
            
            if answer_count > 0:
                # Look for readable service names in the response
                decoded = response[12:].decode('utf-8', errors='ignore')
                services: List[str] = []
                
                # Look for common Apple/Bonjour service patterns
                if '_airplay' in decoded.lower():
                    services.append('AirPlay')
                if '_http' in decoded.lower():
                    services.append('HTTP')
                if '_ssh' in decoded.lower():
                    services.append('SSH')
                if '_printer' in decoded.lower():
                    services.append('Printer')
                
                if services:
                    device_type = "Apple Device" if "_airplay" in decoded.lower() else "mDNS Device"
                    return {
                        "device_name": f"mDNS-{len(services)}-services",
                        "device_type": device_type,
                        "services": services
                    }
        
        except (struct.error, UnicodeDecodeError):
            pass
        
        return None
