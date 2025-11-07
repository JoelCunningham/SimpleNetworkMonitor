import socket
import threading
from datetime import datetime

from mac_vendor_lookup import MacLookup  # type: ignore
from scapy.all import ARP, Ether, get_if_addr, get_if_list, srp  # type: ignore
from scapy.packet import Packet

from app import config
from app.common.constants import *
from app.common.objects import AddressData
from app.common.utilities import Time, time_operation
from app.database.interfaces import DatabaseInterface
from app.database.models import Mac
from app.services.interfaces import MacServiceInterface


class MacService(MacServiceInterface):
    """Service for handling MAC address related operations."""
    
    def __init__(self, database: DatabaseInterface) -> None:
        self.database = database
        self.lock = threading.Lock()

    def save_mac(self, address_data: AddressData, preserve: bool = False) -> Mac:
        if address_data.mac_address is None:
            raise Exception("AddressData does not contain a MAC address.")
    
        mac = self.get_mac_by_address(address_data.mac_address)
        
        if mac:
            mac.ping_time_ms = address_data.ping_time_ms
            mac.arp_time_ms = address_data.arp_time_ms
            mac.last_ip = address_data.ip_address
            mac.last_seen = datetime.now()
            
            if preserve:
                mac.hostname = address_data.hostname or mac.hostname
                mac.vendor = address_data.mac_vendor or mac.vendor
                mac.os_guess = address_data.os_guess or mac.os_guess
                mac.ttl = address_data.ttl or mac.ttl
            else:
                mac.hostname = address_data.hostname
                mac.vendor = address_data.mac_vendor
                mac.os_guess = address_data.os_guess
                mac.ttl = address_data.ttl
                
            self.database.update(mac)
            
        else:
            mac = Mac(
                address=address_data.mac_address,
                ping_time_ms=address_data.ping_time_ms,
                arp_time_ms=address_data.arp_time_ms,
                last_ip=address_data.ip_address,
                hostname=address_data.hostname,
                vendor=address_data.mac_vendor,
                os_guess=address_data.os_guess,
                ttl=address_data.ttl,
                last_seen=datetime.now()
            )

            self.database.create(mac)

        return mac
    
    def get_mac_by_address(self, mac_address: str) -> Mac | None:
        return self.database.select(Mac).where(Mac.address == mac_address).first()

    def resolve_mac_address(self, ip_address: str) -> tuple[str, int] | None:
        arp: Packet = ARP(pdst=ip_address)  # type: ignore
        ether: Packet = Ether(dst=BROADCAST_MAC_ADDRESS)  # type: ignore
        packet: Packet = ether / arp  # type: ignore
        
        iface = self._find_interface(self._get_local_ip())
        
        timeout = config.arp_timeout_ms / 1000

        arp_time = Time()
        with self.lock:
            with time_operation(arp_time):
                try:
                    results = srp(packet, iface=iface, timeout=timeout, verbose=0)[0]  # type: ignore
                except Exception as e:
                    print(f"WARN arp lookup error for {ip_address}: {e}")
                    return None

        if results:
            received_pkt = results[0][1]
            mac_address = getattr(received_pkt, MAC_ADDRESS_ATTR, None)
            if mac_address and isinstance(mac_address, str):
                return (mac_address.lower(), int(arp_time.value))
        
        return None

    def get_vendor_from_mac(self, mac_address: str) -> str | None:
        if not mac_address or len(mac_address) < MAC_OUI_LENGTH:
            return None
        
        try:
            return str(MacLookup().lookup(mac_address))  # type: ignore
            
        except Exception:
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