"""Interfaces for device enrichment services."""
from abc import ABC, abstractmethod
from typing import Optional


class IHostnameResolver(ABC):
    """Interface for hostname resolution."""
    
    @abstractmethod
    def resolve_hostname(self, ip_address: str) -> Optional[str]:
        """Resolve hostname from IP address."""
        pass


class IMacVendorLookup(ABC):
    """Interface for MAC vendor lookup."""
    
    @abstractmethod
    def get_vendor(self, mac_address: str) -> Optional[str]:
        """Get vendor information from MAC address."""
        pass


class IOperatingSystemDetector(ABC):
    """Interface for OS detection."""
    
    @abstractmethod
    def detect_from_ttl(self, ttl: int) -> Optional[str]:
        """Detect OS from TTL value."""
        pass


class IDeviceEnrichmentService(ABC):
    """Interface for comprehensive device enrichment."""
    
    @abstractmethod
    def enrich_device_data(self, ip_address: str, mac_address: Optional[str] = None, 
                          ttl: Optional[int] = None) -> dict[str, Optional[str]]:
        """
        Enrich device with hostname, vendor, and OS information.
        Returns: {"hostname": str, "vendor": str, "os_guess": str}
        """
        pass
