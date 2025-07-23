from dataclasses import dataclass


@dataclass
class ScanOptions:
    """Configuration options for network scanning operations."""
    
    mac_resolution: bool = False
    ttl_resolution: bool = False
    hostname_resolution: bool = False
    mac_vendor_lookup: bool = False
    os_detection: bool = False
    port_scan: bool = False
    detect_http: bool = False
    detect_ssh: bool = False
    detect_banners: bool = False
    discover_netbios: bool = False
    discover_upnp: bool = False
    discover_mdns: bool = False
    
    @classmethod
    def mac_only(cls) -> 'ScanOptions':
        """Create scan options for MAC resolution only."""
        return cls(mac_resolution=True)
    
    @classmethod
    def full_scan(cls) -> 'ScanOptions':
        """Create scan options for full comprehensive scanning."""
        return cls(
            mac_resolution=True,
            ttl_resolution=True,
            hostname_resolution=True,
            mac_vendor_lookup=True,
            os_detection=True,
            port_scan=True,
            detect_http=True,
            detect_ssh=True,
            detect_banners=True,
            discover_netbios=True,
            discover_upnp=True,
            discover_mdns=True
        )
