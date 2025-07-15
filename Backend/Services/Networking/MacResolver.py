import socket
import threading
from typing import Optional, Tuple

from scapy.all import ARP, Ether, get_if_addr, get_if_list, srp  # type: ignore
from scapy.packet import Packet

from Backend.Constants import BROADCAST_MAC_ADDRESS, MAC_ADDRESS_ATTR
from Backend.Objects.Injectable import Injectable
from Backend.Services.AppConfiguration import AppConfig
from Backend.Utilities.Timer import Time, time_operation


class MacResolver(Injectable):
    """Service responsible for ARP resolution."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._lock = threading.Lock()
    
    def resolve_mac_address(self, ip_address: str) -> Optional[Tuple[str, int]]:
        """Resolve MAC address for IP."""        
        arp: Packet = ARP(pdst=ip_address)  # type: ignore
        ether: Packet = Ether(dst=BROADCAST_MAC_ADDRESS)  # type: ignore
        packet: Packet = ether / arp  # type: ignore
        
        iface = self._find_interface(self._get_local_ip())

        arp_time = Time()
        with self._lock:
            with time_operation(arp_time):
                try:
                    results = srp(packet, iface=iface, timeout=self._config.timeout.arp_timeout_s(), verbose=0)[0]   # type: ignore
                except Exception as e:
                    print(f"WARN arp lookup error for {ip_address}: {e}")
                    return None

        if results:
            received_pkt = results[0][1]
            mac_address = getattr(received_pkt, MAC_ADDRESS_ATTR, None)
            if mac_address and isinstance(mac_address, str):
                return (mac_address.lower(), int(arp_time.value))
        
        return None

    def _get_local_ip(self) -> str:
        """Returns the local IP address used to reach the internet."""
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
        finally:
            s.close()

    def _find_interface(self, ip_address: str) -> str | None:
        """Finds the interface that has the given IP address."""
        for iface in get_if_list():
            try:
                if get_if_addr(iface) == ip_address:
                    return iface
            except Exception:
                continue
        return None