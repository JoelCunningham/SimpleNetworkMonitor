import socket
from typing import Optional, Dict

from mac_vendor_lookup import MacLookup  # type: ignore

import Constants
from Objects.Injectable import Injectable
from Services.AppConfig import AppConfig


class EnrichmentService(Injectable):
    """Service for enriching device data with hostname, vendor, and OS information."""
    
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._mac_lookup = None
        self._mac_vendor_cache: Dict[str, str] = {}
        self._load_mac_vendor_database()
    
    def resolve_hostname(self, ip_address: str) -> Optional[str]:
        """Resolve hostname from IP address."""
        try:
            socket.setdefaulttimeout(self.config.hostname_timeout_ms / 1000.0)
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname
        except (socket.herror, socket.gaierror, socket.timeout):
            return None
        finally:
            socket.setdefaulttimeout(None)
    
    def get_mac_vendor(self, mac_address: str) -> Optional[str]:
        """Get vendor information from MAC address using mac-vendor-lookup."""
        if not mac_address:
            return None
        
        try:
            if self._mac_lookup is None:
                self._mac_lookup = MacLookup()
            
            vendor = str(self._mac_lookup.lookup(mac_address))  # type: ignore
            return vendor
            
        except Exception:
            if len(mac_address) < 6:
                return None
            
            oui = mac_address.replace(":", "").replace("-", "").upper()[:6]
            print(f"mac-vendor-lookup failed for {mac_address}, using fallback for OUI {oui}")
            return self._mac_vendor_cache.get(oui, None)
    
    def guess_os_from_ttl(self, ttl: int) -> Optional[str]:
        """Guess operating system based on TTL value."""
        
        if ttl in Constants.TTL_OS_MAPPING:
            return Constants.TTL_OS_MAPPING[ttl]
        
        for expected_ttl, os_name in Constants.TTL_OS_MAPPING.items():
            if expected_ttl - 10 <= ttl <= expected_ttl:
                return f"{os_name} (via router)"
        
        return f"Unknown (TTL: {ttl})"
    
    def _load_mac_vendor_database(self) -> None:
        """Load a minimal MAC vendor database as fallback."""
        self._mac_vendor_cache = {
            "00:03:93": "Apple",
            "00:1A:11": "Google", 
            "00:0D:3A": "Microsoft",
            "00:07:AB": "Samsung",
            "00:03:47": "Intel",
            "00:27:19": "TP-Link",
            "00:09:5B": "Netgear",
            "00:06:25": "Linksys",
            "00:01:42": "Cisco"
        }
