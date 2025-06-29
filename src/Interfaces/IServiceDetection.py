"""Interfaces for service detection and discovery."""
from abc import ABC, abstractmethod
from typing import List, Optional

from Objects.ServiceInfo import ServiceInfo
from Objects.DiscoveryInfo import DiscoveryInfo


class IServiceDetector(ABC):
    """Interface for detecting services on open ports."""
    
    @abstractmethod
    def detect_service(self, ip_address: str, port: int, protocol: str = "tcp") -> Optional[ServiceInfo]:
        """Detect service running on specific port."""
        pass


class IHttpServiceDetector(IServiceDetector):
    """Interface for HTTP service detection."""
    pass


class ISshServiceDetector(IServiceDetector):
    """Interface for SSH service detection."""
    pass


class IBannerGrabber(ABC):
    """Interface for generic banner grabbing."""
    
    @abstractmethod
    def grab_banner(self, ip_address: str, port: int) -> Optional[str]:
        """Grab banner from service."""
        pass


class IDiscoveryProtocol(ABC):
    """Interface for network discovery protocols."""
    
    @abstractmethod
    def discover(self, ip_address: str) -> Optional[DiscoveryInfo]:
        """Discover device information using this protocol."""
        pass
    
    @abstractmethod
    def get_protocol_name(self) -> str:
        """Get the name of this discovery protocol."""
        pass


class IDeviceDiscoveryService(ABC):
    """Interface for device discovery services."""
    
    @abstractmethod
    def discover_device(self, ip_address: str) -> List[DiscoveryInfo]:
        """Discover device using all available protocols."""
        pass
    
    @abstractmethod
    def register_protocol(self, protocol: IDiscoveryProtocol) -> None:
        """Register a discovery protocol."""
        pass
