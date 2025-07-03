from typing import Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet

from Backend.Constants import BROADCAST_MAC_ADDRESS, MAC_ADDRESS_ATTR
from Backend.Objects.Injectable import Injectable
from Backend.Services.AppConfiguration import AppConfig
from Backend.Utilities.Timer import Time, time_operation


class MacResolver(Injectable):
    """Service responsible for ARP resolution."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
    
    def resolve_mac_address(self, ip_address: str) -> Optional[Tuple[str, int]]:
        """
        Resolve MAC address for IP.
        """        
        arp: Packet = ARP(pdst=ip_address)  # type: ignore
        ether: Packet = Ether(dst=BROADCAST_MAC_ADDRESS)  # type: ignore
        packet: Packet = ether / arp  # type: ignore

        arp_time = Time()
        with time_operation(arp_time):
            try:
                results = srp(packet, timeout=self._config.timeout.arp_timeout_s(), verbose=0)[0]   # type: ignore
            except Exception as e:
                print(f"ARP lookup error for {ip_address}: {e}")
                return None

        if results:
            received_pkt = results[0][1]
            mac_address = getattr(received_pkt, MAC_ADDRESS_ATTR, None)
            if mac_address and isinstance(mac_address, str):
                return (mac_address.lower(), int(arp_time.value))
        
        return None
