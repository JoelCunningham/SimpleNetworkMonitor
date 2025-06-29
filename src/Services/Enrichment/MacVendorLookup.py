from typing import Optional

from mac_vendor_lookup import MacLookup  # type: ignore

from Constants import MAC_OUI_LENGTH, MAC_VENDOR_FALLBACK_MAPPING
from Objects.Injectable import Injectable


class MacVendorLookup(Injectable):
    """Service responsible for MAC vendor lookup."""
    
    def __init__(self, mac_lookup: MacLookup) -> None:
        self._mac_lookup = mac_lookup
    
    def get_vendor(self, mac_address: str) -> Optional[str]:
        """Get vendor information from MAC address."""
        if not mac_address or len(mac_address) < MAC_OUI_LENGTH:
            return None
        
        try:
            return str(self._mac_lookup.lookup(mac_address))  # type: ignore
            
        except Exception:
            identifier = mac_address.replace(":", "").replace("-", "").upper()[:MAC_OUI_LENGTH]
            print(f"WARN mac-vendor-lookup failed for {mac_address}, using fallback")
            return MAC_VENDOR_FALLBACK_MAPPING.get(identifier, None)