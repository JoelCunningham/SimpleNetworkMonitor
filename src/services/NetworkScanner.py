import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet

import Constants
import Exceptions
from Objects.AddressData import AddressData
from Objects.Injectable import Injectable
from Services.AppConfig import AppConfig
from Utilities.Timer import Time, time_operation


class NetworkScanner(Injectable):
    _config: AppConfig
    _ping_cmd: str
    _ping_count_flag: str
    _ping_timeout_flag: str
    _ping_timeout_value: float
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        
        system = platform.system()
        if system not in Constants.PING_COMMANDS:
            raise Exceptions.NetworkScanError(f"Unsupported operating system: {system}")
        
        if system == Constants.PLATFORM_WINDOWS:
            self._ping_timeout_value = int(config.ping_timeout_ms)
        else:
            self._ping_timeout_value = config.ping_timeout_ms / 1000
        
        self._ping_cmd = Constants.PING_COMMANDS[system]["cmd"]
        self._ping_count_flag = Constants.PING_COMMANDS[system]["count_flag"]
        self._ping_timeout_flag = Constants.PING_COMMANDS[system]["timeout_flag"]
        
                
    def scan_network(self) -> List[AddressData]:
        devices: List[AddressData] = []
        ip_range: List[str] = [f"{self._config.subnet}.{i}" for i in range(self._config.min_ip, self._config.max_ip + 1)]

        with ThreadPoolExecutor(max_workers=self._config.max_threads) as executor:
            futures = [executor.submit(self.scan_ip, ip) for ip in ip_range]
            for future in as_completed(futures):
                device: Optional[AddressData] = future.result()
                if device is not None:
                    devices.append(device)
        return devices

    def scan_ip(self, ip_address: str) -> Optional[AddressData]:
        ping_time = Time()
        with time_operation(ping_time):
            try:
                result = subprocess.call(
                    [
                        self._ping_cmd,
                        self._ping_count_flag, str(self._config.ping_count),
                        self._ping_timeout_flag, str(self._ping_timeout_value),
                        ip_address
                    ],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
                print(f"Ping error for {ip_address}: {e}")
                return None

        if result != Constants.SUCCESSFUL_PING_EXIT_CODE:
            return None

        mac, arp_time = self.lookup_arp(ip_address)

        return AddressData(
            mac_address=mac, 
            ip_address=ip_address, 
            ping_time_ms=int(ping_time.value), 
            arp_time_ms=int(arp_time.value),
        )

    def lookup_arp(self, ip: str) -> Tuple[Optional[str], Time]:
        arp: Packet = ARP(pdst=ip)  # type: ignore
        ether: Packet = Ether(dst=Constants.BROADCAST_MAC_ADDRESS)  # type: ignore
        packet: Packet = ether / arp  # type: ignore

        arp_time = Time()
        with time_operation(arp_time):
            try:
                results = srp(packet, timeout=self._config.arp_timeout_ms/1000, verbose=0)[0]  # type: ignore
            except Exception as e:
                print(f"ARP lookup error for {ip}: {e}")
                return None, arp_time

        if results:
            received_pkt = results[0][1]
            mac_address = getattr(received_pkt, "hwsrc", None)
            if mac_address and isinstance(mac_address, str):
                return mac_address.lower(), arp_time
        return None, arp_time
