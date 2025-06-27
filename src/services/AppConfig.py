import json
import os
from typing import Any, Dict

import Constants
import Exceptions
from Objects.Injectable import Injectable


class AppConfig(Injectable):
    database: str
    subnet: str
    min_ip: int
    max_ip: int
    max_threads: int
    ping_count: int
    ping_timeout_ms: int
    arp_timeout_ms: int
    hostname_timeout_ms: int
    
    mac_resolution: bool
    hostname_resolution: bool
    mac_vendor_lookup: bool
    os_detection: bool

    def __init__(self, filepath: str) -> None:
        if not os.path.exists(filepath):
            raise Exceptions.ConfigurationError(Constants.CONFIG_FILE_NOT_FOUND.format(filepath=filepath))
        try:
            with open(filepath, "r", encoding=Constants.DEFAULT_ENCODING) as file:
                data: Dict[str, Any] = json.load(file)
                
                required_fields = [
                    "database", 
                    "subnet", 
                    "min_ip", 
                    "max_ip", 
                    "max_threads", 
                    "ping_count", 
                    "ping_timeout_ms", 
                    "arp_timeout_ms"
                ]
                missing_fields = [field for field in required_fields if field not in data]
                
                if missing_fields:
                    raise Exceptions.ConfigurationError(Constants.CONFIG_MISSING_FIELDS.format(
                        filepath=filepath, 
                        fields=missing_fields
                    ))
                
                self.database = str(data["database"])
                self.subnet = str(data["subnet"])
                self.min_ip = int(data["min_ip"])
                self.max_ip = int(data["max_ip"])
                self.max_threads = int(data["max_threads"])
                self.ping_count = int(data["ping_count"])
                self.ping_timeout_ms = int(data["ping_timeout_ms"])
                self.arp_timeout_ms = int(data["arp_timeout_ms"])
                self.hostname_timeout_ms = int(data["hostname_timeout_ms"])
                
                enrichment = data["enrichment"]
                self.mac_resolution = bool(enrichment["mac_resolution"])
                self.hostname_resolution = bool(enrichment["hostname_resolution"])
                self.mac_vendor_lookup = bool(enrichment["mac_vendor_lookup"])
                self.os_detection = bool(enrichment["os_detection"])
                
                self._validate()
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            raise Exceptions.ConfigurationError(Constants.CONFIG_INVALID.format(filepath=filepath, error=str(e)))
    
    def _validate(self) -> None:
        """Validate configuration values."""
        if self.min_ip < Constants.MIN_IP_ADDRESS or self.min_ip > Constants.MAX_IP_ADDRESS:
            raise Exceptions.ConfigurationError(f"min_ip must be between {Constants.MIN_IP_ADDRESS} and {Constants.MAX_IP_ADDRESS}")
        if self.max_ip < Constants.MIN_IP_ADDRESS or self.max_ip > Constants.MAX_IP_ADDRESS:
            raise Exceptions.ConfigurationError(f"max_ip must be between {Constants.MIN_IP_ADDRESS} and {Constants.MAX_IP_ADDRESS}")
        if self.min_ip > self.max_ip:
            raise Exceptions.ConfigurationError("min_ip cannot be greater than max_ip")
        if self.max_threads < Constants.MIN_THREADS:
            raise Exceptions.ConfigurationError("max_threads must be positive")
        if self.ping_count < Constants.MIN_PING_COUNT:
            raise Exceptions.ConfigurationError("ping_count must be positive")
        if self.ping_timeout_ms < Constants.MIN_TIMEOUT_MS:
            raise Exceptions.ConfigurationError("ping_timeout_ms must be positive")
        if self.arp_timeout_ms < Constants.MIN_TIMEOUT_MS:
            raise Exceptions.ConfigurationError("arp_timeout_ms must be positive")
        if self.hostname_timeout_ms < Constants.MIN_TIMEOUT_MS:
            raise Exceptions.ConfigurationError("hostname_timeout_ms must be positive")
