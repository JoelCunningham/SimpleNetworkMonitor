"""Device enrichment services."""
from typing import Optional

from Constants import ROUTER_TTL_TEMPLATE, TTL_OS_MAPPING, UNKNOWN_OS_TEMPLATE
from Objects.Injectable import Injectable


class OperatingSystemLookup(Injectable):
    """Service responsible for OS detection from TTL values."""
    
    def detect_from_ttl(self, ttl: int) -> Optional[str]:
        """Detect operating system based on TTL value."""
        if ttl in TTL_OS_MAPPING:
            return TTL_OS_MAPPING[ttl]
        
        # Check for TTL values that might have passed through routers
        for expected_ttl, os_name in TTL_OS_MAPPING.items():
            if expected_ttl - 10 <= ttl <= expected_ttl:
                return ROUTER_TTL_TEMPLATE.format(os_name=os_name)
        
        return UNKNOWN_OS_TEMPLATE.format(ttl=ttl)