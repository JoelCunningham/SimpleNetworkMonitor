"""Interfaces for data persistence operations."""
from abc import ABC, abstractmethod
from typing import List, Optional, Any, Dict

from sqlmodel import Session
from Objects.AddressData import AddressData
from Models.MacModel import Mac


class IDatabaseConnection(ABC):
    """Interface for database connection management."""
    
    @abstractmethod
    def get_session(self) -> Session:
        """Get database session."""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close database connection."""
        pass


class IDeviceRepository(ABC):
    """Interface for device data persistence."""
    
    @abstractmethod
    def save_device(self, address_data: AddressData) -> Mac:
        """Save or update device data."""
        pass
    
    @abstractmethod
    def get_device_by_mac(self, mac_address: str) -> Optional[Mac]:
        """Get device by MAC address."""
        pass
    
    @abstractmethod
    def get_all_devices(self) -> List[Mac]:
        """Get all known devices."""
        pass


class IScanDataRepository(ABC):
    """Interface for scan data persistence."""
    
    @abstractmethod
    def save_scan_results(self, mac: Mac, address_data: AddressData) -> None:
        """Save comprehensive scan results."""
        pass
    
    @abstractmethod
    def get_scan_history(self, mac: Mac) -> List[Dict[str, Any]]:
        """Get scan history for device."""
        pass
