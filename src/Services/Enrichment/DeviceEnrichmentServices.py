"""Device enrichment services."""
import socket
from typing import Optional, Dict

from mac_vendor_lookup import MacLookup  # type: ignore

import Constants
from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.IEnrichment import (
    IHostnameResolver, IMacVendorLookup, IOperatingSystemDetector, IDeviceEnrichmentService
)
from Objects.Injectable import Injectable


class HostnameResolver(IHostnameResolver, Injectable):
    """Service responsible for hostname resolution."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def resolve_hostname(self, ip_address: str) -> Optional[str]:
        """Resolve hostname from IP address."""
        timeout_settings = self._config_provider.get_timeout_settings()
        timeout_seconds = timeout_settings["hostname_timeout_ms"] / 1000.0
        
        try:
            socket.setdefaulttimeout(timeout_seconds)
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname
        except (socket.herror, socket.gaierror, socket.timeout):
            return None
        finally:
            socket.setdefaulttimeout(None)


class MacVendorLookupService(IMacVendorLookup, Injectable):
    """Service responsible for MAC vendor lookup."""
    
    def __init__(self) -> None:
        self._mac_lookup: Optional[MacLookup] = None
        self._vendor_cache: Dict[str, str] = Constants.MAC_VENDOR_FALLBACK_MAPPING
    
    def get_vendor(self, mac_address: str) -> Optional[str]:
        """Get vendor information from MAC address."""
        if not mac_address or len(mac_address) < 6:
            return None
        
        try:
            if self._mac_lookup is None:
                self._mac_lookup = MacLookup()
            
            vendor = str(self._mac_lookup.lookup(mac_address))  # type: ignore
            return vendor
            
        except Exception:
            # Fall back to OUI cache
            oui = mac_address.replace(":", "").replace("-", "").upper()[:6]
            print(f"mac-vendor-lookup failed for {mac_address}, using fallback for OUI {oui}")
            return self._vendor_cache.get(oui, None)


class OperatingSystemDetector(IOperatingSystemDetector, Injectable):
    """Service responsible for OS detection from TTL values."""
    
    def detect_from_ttl(self, ttl: int) -> Optional[str]:
        """Detect operating system based on TTL value."""
        if ttl in Constants.TTL_OS_MAPPING:
            return Constants.TTL_OS_MAPPING[ttl]
        
        # Check for TTL values that might have passed through routers
        for expected_ttl, os_name in Constants.TTL_OS_MAPPING.items():
            if expected_ttl - 10 <= ttl <= expected_ttl:
                return f"{os_name} (via router)"
        
        return f"Unknown (TTL: {ttl})"


class DeviceEnrichmentService(IDeviceEnrichmentService, Injectable):
    """Composite service for comprehensive device enrichment."""
    
    def __init__(self, hostname_resolver: IHostnameResolver, 
                 vendor_lookup: IMacVendorLookup, 
                 os_detector: IOperatingSystemDetector,
                 config_provider: IConfigurationProvider) -> None:
        self._hostname_resolver = hostname_resolver
        self._vendor_lookup = vendor_lookup
        self._os_detector = os_detector
        self._config_provider = config_provider
    
    def enrich_device_data(self, ip_address: str, mac_address: Optional[str] = None, 
                          ttl: Optional[int] = None) -> Dict[str, Optional[str]]:
        """
        Enrich device with hostname, vendor, and OS information.
        Returns: {"hostname": str, "vendor": str, "os_guess": str}
        """
        feature_flags = self._config_provider.get_feature_flags()
        
        result: Dict[str, Optional[str]] = {
            "hostname": None,
            "vendor": None,
            "os_guess": None
        }
        
        # Resolve hostname if enabled
        if feature_flags.get("hostname_resolution", False):
            result["hostname"] = self._hostname_resolver.resolve_hostname(ip_address)
        
        # Lookup MAC vendor if enabled and MAC address is available
        if feature_flags.get("mac_vendor_lookup", False) and mac_address:
            result["vendor"] = self._vendor_lookup.get_vendor(mac_address)
        
        # Detect OS if enabled and TTL is available
        if feature_flags.get("os_detection", False) and ttl is not None:
            result["os_guess"] = self._os_detector.detect_from_ttl(ttl)
        
        return result
