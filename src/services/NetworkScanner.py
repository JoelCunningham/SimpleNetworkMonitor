import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet

from objects.AppConfig import AppConfig
from objects.NetworkDevice import NetworkDevice
from services.DeviceResolver import DeviceResolver


class NetworkScanner:
    SUCCESSFUL_EXIT_CODE: int = 0
    
    def __init__(self, config: AppConfig, resolver: DeviceResolver) -> None:
        self.subnet = config.subnet
        self.resolver = resolver
        self.max_threads = config.max_threads
        self.ping_count = config.ping_count
        self.ping_timeout_ms = config.ping_timeout_ms
        self.arp_timeout_s = config.arp_timeout_s
        
    def scan_network(self) -> List[NetworkDevice]:
        ip_range: List[str] = [f"{self.subnet}.{i}" for i in range(1, 255)]
        devices: List[NetworkDevice] = []

        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip) for ip in ip_range]
            for future in as_completed(futures):
                device: Optional[NetworkDevice] = future.result()
                if device is not None:
                    devices.append(device)
                    print(
                        f"{device.ip} - {device.mac} - {device.name} | "
                        f"ping: {device.ping_time_ms}ms | arp: {device.arp_time_ms}ms"
                    )
        return devices

    def scan_ip(self, ip: str) -> Optional[NetworkDevice]:
        ping_start: float = time.time()
        retcode: int = subprocess.call(
            ["ping", "-n", str(self.ping_count), "-w", str(self.ping_timeout_ms), ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        ping_elapsed: float = (time.time() - ping_start) * 1000

        if retcode != self.SUCCESSFUL_EXIT_CODE:
            return None

        mac, arp_elapsed = self.arp_lookup(ip)
        if mac is None:
            print(f"ARP lookup failed for {ip}")
            return None

        name: str = self.resolver.resolve_name(mac)
        return NetworkDevice(ip=ip, mac=mac, name=name, ping_time_ms=round(ping_elapsed, 1), arp_time_ms=round(arp_elapsed, 1))

    def arp_lookup(self, ip: str) -> Tuple[Optional[str], float]:
        arp: Packet = ARP(pdst=ip)  # type: ignore
        ether: Packet = Ether(dst="ff:ff:ff:ff:ff:ff")  # type: ignore
        packet: Packet = ether / arp  # type: ignore

        arp_start: float = time.time()
        result_list = srp(packet, timeout=self.arp_timeout_s, verbose=0)[0]  # type: ignore
        arp_elapsed: float = (time.time() - arp_start) * 1000

        if result_list:
            received_pkt = result_list[0][1]
            mac_address = getattr(received_pkt, "hwsrc", None)
            if isinstance(mac_address, str):
                return mac_address.lower(), arp_elapsed
        return None, arp_elapsed
