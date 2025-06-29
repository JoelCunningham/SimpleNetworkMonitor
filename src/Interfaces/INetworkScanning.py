"""Interfaces for network scanning operations."""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from Objects.AddressData import AddressData
from Objects.PortInfo import PortInfo


class INetworkPinger(ABC):
    """Interface for network ping operations."""
    
    @abstractmethod
    def ping(self, ip_address: str) -> Optional[tuple[bool, int, Optional[str]]]:
        """
        Ping an IP address.
        Returns: (success, response_time_ms, stdout)
        """
        pass


class IArpResolver(ABC):
    """Interface for ARP resolution operations."""
    
    @abstractmethod
    def resolve_mac_address(self, ip_address: str) -> Optional[tuple[str, int]]:
        """
        Resolve MAC address for IP.
        Returns: (mac_address, resolution_time_ms)
        """
        pass


class IPortScanner(ABC):
    """Interface for port scanning operations."""
    
    @abstractmethod
    def scan_ports(self, ip_address: str, ports: List[int]) -> List[PortInfo]:
        """Scan specified ports on target IP."""
        pass


class INetworkScanner(ABC):
    """Interface for comprehensive network scanning."""
    
    @abstractmethod
    def scan_network(self) -> List[AddressData]:
        """Scan the configured network range."""
        pass
    
    @abstractmethod
    def scan_ip(self, ip_address: str) -> Optional[AddressData]:
        """Scan a specific IP address."""
        pass
    
    @abstractmethod
    def get_scan_summary(self, address_data: AddressData) -> Dict[str, Any]:
        """Get a summary of scan results for display."""
        pass
