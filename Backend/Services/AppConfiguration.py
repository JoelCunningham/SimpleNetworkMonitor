import json
import os
from typing import Any

from Backend import Exceptions
from Backend.Constants import DEFAULT_ENCODING
from Backend.Objects.Injectable import Injectable


class AppConfig(Injectable):
    """Main configuration provider for the network monitor application."""
    
    def __init__(self, filepath: str) -> None:
        self._config_data = self._load_from_file(filepath)
        self.network = self.Network(self._config_data)
        self.timeout = self.Timeout(self._config_data)
        self.feature = self.Feature(self._config_data)
    
    def _load_from_file(self, filepath: str) -> dict[str, Any]:
        """Load configuration data from JSON file."""
        if not os.path.exists(filepath):
            raise Exceptions.ConfigurationError(f"AppConfig file {filepath} does not exist.")
        
        try:
            with open(filepath, "r", encoding=DEFAULT_ENCODING) as file:
                return json.load(file)
        except (json.JSONDecodeError, ValueError) as e:
            raise Exceptions.ConfigurationError(f"Invalid config in {filepath}") from e
        
    def database_path(self) -> str:
        return str(self._config_data["database"])
    
    class Network():
        """Network configuration settings."""
        def __init__(self, config_data: dict[str, Any]) -> None:
            self._config_data = config_data
        
        def subnet(self) -> str:
            return str(self._config_data["subnet"])        
        def min_ip(self) -> int:
            return int(self._config_data["min_scan_ip"])     
        def max_ip(self) -> int:
            return int(self._config_data["max_scan_ip"])      
        def ping_count(self) -> int:
            return int(self._config_data["ping_count"])
        def max_threads(self) -> int:
            return int(self._config_data["max_threads"])
    
    class Timeout():
        """Timeout settings for various operations."""
        def __init__(self, config_data: dict[str, Any]) -> None:
            self._config_data = config_data
        
        def ping_timeout_ms(self) -> int:
            return int(self._config_data["ping_timeout_ms"])   
        def ping_timeout_s(self) -> int:
            return int(self._config_data["ping_timeout_ms"] / 1000)   
        def arp_timeout_s(self) -> int:
            return int(self._config_data["arp_timeout_ms"] / 1000)
        def hostname_timeout_s(self) -> int:
            return int(self._config_data["hostname_timeout_ms"] / 1000)
        def port_scan_timeout_s(self) -> int:
            return int(self._config_data["port_scan_timeout_ms"] / 1000)
        def service_detection_timeout_s(self) -> int:
            return int(self._config_data["service_detection_timeout_ms"] / 1000)
        def discovery_timeout_s(self) -> int:
            return int(self._config_data["discovery_timeout_ms"] / 1000)

    class Feature():
        """Feature flags for various functionalities."""
        def __init__(self, config_data: dict[str, Any]) -> None:
            self._config_data = config_data
            
        def mac_resolution_enabled(self) -> bool:
            return bool(self._config_data["mac_resolution"])
        def hostname_resolution_enabled(self) -> bool:
            return bool(self._config_data["hostname_resolution"])
        def ttl_resolution_enabled(self) -> bool:
            return bool(self._config_data["ttl_resolution"])
        def mac_vendor_lookup_enabled(self) -> bool:
            return bool(self._config_data["mac_vendor_lookup"])
        def os_detection_enabled(self) -> bool:
            return bool(self._config_data["os_detection"])
        def port_scan_enabled(self) -> bool:
            return bool(self._config_data["port_scan"])
        def detect_http_enabled(self) -> bool:
            return bool(self._config_data.get("detect_http", True))
        def detect_ssh_enabled(self) -> bool:
            return bool(self._config_data.get("detect_ssh", True))
        def detect_banners_enabled(self) -> bool:
            return bool(self._config_data.get("detect_banners", True))
        def discover_netbios_enabled(self) -> bool:
            return bool(self._config_data.get("discover_netbios", True))
        def discover_upnp_enabled(self) -> bool:
            return bool(self._config_data.get("discover_upnp", True))
        def discover_mdns_enabled(self) -> bool:
            return bool(self._config_data.get("discover_mdns", True))
    