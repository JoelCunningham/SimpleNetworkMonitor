"""Discovery protocol implementations."""
import socket
import struct
from typing import List, Optional, Dict

from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.IServiceDetection import IDiscoveryProtocol, IDeviceDiscoveryService
from Objects.DiscoveryInfo import DiscoveryInfo
from Objects.Injectable import Injectable


class NetBiosDiscoveryProtocol(IDiscoveryProtocol, Injectable):
    """NetBIOS discovery protocol implementation."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def get_protocol_name(self) -> str:
        """Get the name of this discovery protocol."""
        return "netbios"
    
    def discover(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using NetBIOS Name Service."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["discovery_timeout_ms"] / 1000
        
        try:
            # NetBIOS Name Service query (port 137/udp)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout_seconds)
            
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
                
                if len(response) > 12:
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


class UpnpDiscoveryProtocol(IDiscoveryProtocol, Injectable):
    """UPnP/SSDP discovery protocol implementation."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def get_protocol_name(self) -> str:
        """Get the name of this discovery protocol."""
        return "upnp"
    
    def discover(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using UPnP/SSDP."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["discovery_timeout_ms"] / 1000
        
        try:
            # Send SSDP M-SEARCH request
            ssdp_request = (
                "M-SEARCH * HTTP/1.1\r\n"
                "HOST: 239.255.255.250:1900\r\n"
                'MAN: "ssdp:discover"\r\n'
                "ST: upnp:rootdevice\r\n"
                f"MX: {int(timeout_seconds)}\r\n"
                "\r\n"
            ).encode('utf-8')
            
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout_seconds)
            
            # Send to specific IP instead of multicast for targeted discovery
            sock.sendto(ssdp_request, (ip_address, 1900))
            
            try:
                response, _ = sock.recvfrom(1024)
                response_text = response.decode('utf-8', errors='ignore')
                
                if "HTTP/1.1 200 OK" in response_text:
                    device_info = self._parse_upnp_response(response_text)
                    if device_info:
                        return DiscoveryInfo(
                            protocol="upnp",
                            device_name=device_info.get("device_name"),
                            device_type=device_info.get("device_type", "UPnP Device")
                        )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, UnicodeDecodeError):
            pass
        
        return None
    
    def _parse_upnp_response(self, response: str) -> Optional[Dict[str, str]]:
        """Parse UPnP response to extract device information."""
        try:
            lines = response.split('\r\n')
            device_info: Dict[str, str] = {}
            
            for line in lines:
                if line.startswith('SERVER:'):
                    device_info["device_name"] = line.split(':', 1)[1].strip()
                elif line.startswith('ST:'):
                    device_info["device_type"] = line.split(':', 1)[1].strip()
            
            return device_info if device_info else None
        except (IndexError, AttributeError):
            return None


class MdnsDiscoveryProtocol(IDiscoveryProtocol, Injectable):
    """mDNS/Bonjour discovery protocol implementation."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def get_protocol_name(self) -> str:
        """Get the name of this discovery protocol."""
        return "mdns"
    
    def discover(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using mDNS."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["discovery_timeout_ms"] / 1000
        
        try:
            # Simple mDNS query - this is a basic implementation
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(timeout_seconds)
            
            # mDNS query for _services._dns-sd._udp.local
            query_packet = struct.pack('>HHHHHH', 
                0x0000,  # Transaction ID
                0x0000,  # Flags
                1,       # Questions
                0,       # Answer RRs
                0,       # Authority RRs
                0        # Additional RRs
            )
            
            # Add the query for services enumeration
            # This is a simplified implementation
            service_query = b'\x09_services\x07_dns-sd\x04_udp\x05local\x00\x00\x0c\x00\x01'
            query_packet += service_query
            
            sock.sendto(query_packet, (ip_address, 5353))
            
            try:
                response, _ = sock.recvfrom(1024)
                
                if len(response) > 12:
                    # Basic parsing - in a real implementation, this would be more sophisticated
                    if b'_http._tcp' in response or b'_device-info._tcp' in response:
                        return DiscoveryInfo(
                            protocol="mdns",
                            device_name=f"mDNS-{ip_address.split('.')[-1]}",
                            device_type="mDNS/Bonjour Device"
                        )
            
            except socket.timeout:
                pass
            finally:
                sock.close()
        
        except (socket.error, struct.error):
            pass
        
        return None


class DeviceDiscoveryService(IDeviceDiscoveryService, Injectable):
    """Service that orchestrates multiple discovery protocols."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
        self._protocols: List[IDiscoveryProtocol] = []
    
    def register_protocol(self, protocol: IDiscoveryProtocol) -> None:
        """Register a discovery protocol."""
        self._protocols.append(protocol)
    
    def discover_device(self, ip_address: str) -> List[DiscoveryInfo]:
        """Discover device using all available protocols."""
        feature_flags = self._config_provider.get_feature_flags()
        discoveries: List[DiscoveryInfo] = []
        
        for protocol in self._protocols:
            protocol_name = protocol.get_protocol_name()
            
            # Check if this protocol is enabled
            feature_key = f"discover_{protocol_name}"
            if not feature_flags.get(feature_key, False):
                continue
            
            try:
                discovery_info = protocol.discover(ip_address)
                if discovery_info:
                    discoveries.append(discovery_info)
            except Exception as e:
                print(f"Error in {protocol_name} discovery for {ip_address}: {e}")
        
        return discoveries
