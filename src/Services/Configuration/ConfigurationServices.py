"""Configuration loading and validation services."""
import json
import os
from typing import Any, Dict

import Constants
import Exceptions
from Interfaces.IConfigurationProvider import IConfigurationProvider
from Objects.Injectable import Injectable


class ConfigurationLoader(Injectable):
    """Responsible for loading configuration from files."""
    
    def load_from_file(self, filepath: str) -> Dict[str, Any]:
        """Load configuration data from JSON file."""
        if not os.path.exists(filepath):
            raise Exceptions.ConfigurationError(
                Constants.CONFIG_FILE_NOT_FOUND.format(filepath=filepath)
            )
        
        try:
            with open(filepath, "r", encoding=Constants.DEFAULT_ENCODING) as file:
                return json.load(file)
        except (json.JSONDecodeError, ValueError) as e:
            raise Exceptions.ConfigurationError(
                Constants.CONFIG_INVALID.format(filepath=filepath, error=str(e))
            ) from e


class ConfigurationValidator(Injectable):
    """Responsible for validating configuration values."""
    
    def validate_network_config(self, config_data: Dict[str, Any]) -> None:
        """Validate network-related configuration."""
        min_ip = config_data.get("min_ip", 0)
        max_ip = config_data.get("max_ip", 0)
        
        if min_ip < Constants.MIN_IP_ADDRESS or min_ip > Constants.MAX_IP_ADDRESS:
            raise Exceptions.ConfigurationError(
                f"min_ip must be between {Constants.MIN_IP_ADDRESS} and {Constants.MAX_IP_ADDRESS}"
            )
        
        if max_ip < Constants.MIN_IP_ADDRESS or max_ip > Constants.MAX_IP_ADDRESS:
            raise Exceptions.ConfigurationError(
                f"max_ip must be between {Constants.MIN_IP_ADDRESS} and {Constants.MAX_IP_ADDRESS}"
            )
        
        if min_ip > max_ip:
            raise Exceptions.ConfigurationError("min_ip cannot be greater than max_ip")
    
    def validate_performance_config(self, config_data: Dict[str, Any]) -> None:
        """Validate performance-related configuration."""
        max_threads = config_data.get("max_threads", 0)
        if max_threads < Constants.MIN_THREADS:
            raise Exceptions.ConfigurationError("max_threads must be positive")
    
    def validate_timeout_config(self, config_data: Dict[str, Any]) -> None:
        """Validate timeout-related configuration."""
        timeout_fields = [
            "ping_timeout_ms", "arp_timeout_ms", "hostname_timeout_ms",
            "port_scan_timeout_ms", "service_detection_timeout_ms", "discovery_timeout_ms"
        ]
        
        for field in timeout_fields:
            value = config_data.get(field, 0)
            if value < Constants.MIN_TIMEOUT_MS:
                raise Exceptions.ConfigurationError(f"{field} must be positive")
    
    def validate_ping_config(self, config_data: Dict[str, Any]) -> None:
        """Validate ping-related configuration."""
        ping_count = config_data.get("ping_count", 0)
        if ping_count < Constants.MIN_PING_COUNT:
            raise Exceptions.ConfigurationError("ping_count must be positive")
    
    def validate_required_fields(self, config_data: Dict[str, Any], required_fields: list[str]) -> None:
        """Validate that all required fields are present."""
        missing_fields = [field for field in required_fields if field not in config_data]
        if missing_fields:
            raise Exceptions.ConfigurationError(
                f"Missing required configuration fields: {missing_fields}"
            )


class NetworkMonitorConfiguration(IConfigurationProvider, Injectable):
    """Main configuration provider for the network monitor application."""
    
    def __init__(self, filepath: str, loader: ConfigurationLoader, validator: ConfigurationValidator) -> None:
        self._loader = loader
        self._validator = validator
        self._config_data = self._load_and_validate(filepath)
    
    def _load_and_validate(self, filepath: str) -> Dict[str, Any]:
        """Load and validate configuration."""
        config_data = self._loader.load_from_file(filepath)
        
        # Define required fields
        required_fields = [
            "database", "subnet", "min_ip", "max_ip", "max_threads", 
            "ping_count", "ping_timeout_ms", "arp_timeout_ms"
        ]
        
        # Validate all aspects
        self._validator.validate_required_fields(config_data, required_fields)
        self._validator.validate_network_config(config_data)
        self._validator.validate_performance_config(config_data)
        self._validator.validate_timeout_config(config_data)
        self._validator.validate_ping_config(config_data)
        
        return config_data
    
    def get_database_path(self) -> str:
        """Get database connection string/path."""
        return str(self._config_data["database"])
    
    def get_network_settings(self) -> Dict[str, Any]:
        """Get network scanning settings."""
        return {
            "subnet": str(self._config_data["subnet"]),
            "min_ip": int(self._config_data["min_ip"]),
            "max_ip": int(self._config_data["max_ip"]),
            "ping_count": int(self._config_data["ping_count"])
        }
    
    def get_timeout_settings(self) -> Dict[str, Any]:
        """Get timeout configurations."""
        return {
            "ping_timeout_ms": int(self._config_data["ping_timeout_ms"]),
            "arp_timeout_ms": int(self._config_data["arp_timeout_ms"]),
            "hostname_timeout_ms": int(self._config_data.get("hostname_timeout_ms", 5000)),
            "port_scan_timeout_ms": int(self._config_data.get("port_scan_timeout_ms", 1000)),
            "service_detection_timeout_ms": int(self._config_data.get("service_detection_timeout_ms", 5000)),
            "discovery_timeout_ms": int(self._config_data.get("discovery_timeout_ms", 3000))
        }
    
    def get_feature_flags(self) -> Dict[str, bool]:
        """Get enabled/disabled features."""
        enrichment = self._config_data.get("enrichment", {})
        return {
            "mac_resolution": bool(enrichment.get("mac_resolution", True)),
            "hostname_resolution": bool(enrichment.get("hostname_resolution", True)),
            "mac_vendor_lookup": bool(enrichment.get("mac_vendor_lookup", True)),
            "os_detection": bool(enrichment.get("os_detection", True)),
            "port_scan": bool(enrichment.get("port_scan", True)),
            "detect_http": bool(enrichment.get("detect_http", True)),
            "detect_ssh": bool(enrichment.get("detect_ssh", True)),
            "detect_banners": bool(enrichment.get("detect_banners", True)),
            "discover_netbios": bool(enrichment.get("discover_netbios", True)),
            "discover_upnp": bool(enrichment.get("discover_upnp", True)),
            "discover_mdns": bool(enrichment.get("discover_mdns", True))
        }
    
    def get_performance_settings(self) -> Dict[str, Any]:
        """Get performance-related settings."""
        return {
            "max_threads": int(self._config_data["max_threads"])
        }
