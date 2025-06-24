import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet

from objects.AddressData import AddressData
from objects.AppConfig import AppConfig
from utilities.Timer import Time, time_operation


class NetworkScanner:
    SUCCESSFUL_EXIT_CODE: int = 0
    BROADCAST_MAC: str = "ff:ff:ff:ff:ff:ff"
    NO_MAC_NAME: str = "Unknown"
    PING_COMMAND: str = "ping"
    PING_FLAG_COUNT: str = "-n"
    PING_FLAG_TIMEOUT: str = "-w"

    def __init__(self, config: AppConfig) -> None:
        self.subnet = config.subnet
        self.min_ip = config.min_ip
        self.max_ip = config.max_ip
        
        self.max_threads = config.max_threads
        self.ping_count = config.ping_count
        self.ping_timeout_ms = config.ping_timeout_ms
        self.arp_timeout_ms = config.arp_timeout_ms
                
    def scan_network(self) -> List[AddressData]:
        devices: List[AddressData] = []
        ip_range: List[str] = [f"{self.subnet}.{i}" for i in range(self.min_ip, self.max_ip + 1)]

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip) for ip in ip_range]
            for future in as_completed(futures):
                device: Optional[AddressData] = future.result()
                if device is not None:
                    devices.append(device)
        return devices

    def scan_ip(self, ip_address: str) -> Optional[AddressData]:
        ping_time = Time()
        with time_operation(ping_time):
            result = subprocess.call(
                [
                    self.PING_COMMAND,
                    self.PING_FLAG_COUNT, str(self.ping_count),
                    self.PING_FLAG_TIMEOUT, str(self.ping_timeout_ms),
                    ip_address
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        if result != self.SUCCESSFUL_EXIT_CODE:
            return None

        mac, arp_time = self.lookup_arp(ip_address)

        return AddressData(
            mac=mac, 
            ip=ip_address, 
            ping_time_ms=int(ping_time.value), 
            arp_time_ms=int(arp_time.value),
        )

    def lookup_arp(self, ip: str) -> Tuple[Optional[str], Time]:
        arp: Packet = ARP(pdst=ip)  # type: ignore
        ether: Packet = Ether(dst=self.BROADCAST_MAC)  # type: ignore
        packet: Packet = ether / arp  # type: ignore

        arp_time = Time()
        with time_operation(arp_time):
            results = srp(packet, timeout=self.arp_timeout_ms/1000, verbose=0)[0]  # type: ignore

        if results:
            received_pkt = results[0][1]
            mac_address = getattr(received_pkt, "hwsrc", None)
            if isinstance(mac_address, str):
                return mac_address.lower(), arp_time
        return None, arp_time
