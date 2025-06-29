"""Interface for configuration providers."""
from abc import ABC, abstractmethod
from typing import Any


class IConfigurationProvider(ABC):
    """Interface for providing configuration data."""
    
    @abstractmethod
    def get_database_path(self) -> str:
        """Get database connection string/path."""
        pass
    
    @abstractmethod
    def get_network_settings(self) -> dict[str, Any]:
        """Get network scanning settings."""
        pass
    
    @abstractmethod
    def get_timeout_settings(self) -> dict[str, Any]:
        """Get timeout configurations."""
        pass
    
    @abstractmethod
    def get_feature_flags(self) -> dict[str, bool]:
        """Get enabled/disabled features."""
        pass
    
    @abstractmethod
    def get_performance_settings(self) -> dict[str, Any]:
        """Get performance-related settings."""
        pass
