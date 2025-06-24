import json
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet


@dataclass
class Config:
    subnet: str = "192.168.0"
    max_threads: int = 50
    ping_count: int = 1
    ping_timeout_ms: int = 200
    arp_timeout_s: float = 1.0
    data_file: str = "data.json"

@dataclass
class NetworkDevice:
    ip: str
    mac: str
    name: str
    ping_time_ms: float
    arp_time_ms: float

@staticmethod
def from_json_file(filepath: str) -> "Config":
    if not os.path.exists(filepath):
        return Config()
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data: Dict[str, Any] = json.load(f)
            return Config(
                subnet=data.get("subnet", "192.168.0"),
                max_threads=int(data.get("max_threads", 50)),
                ping_count=int(data.get("ping_count", 1)),
                ping_timeout_ms=int(data.get("ping_timeout_ms", 200)),
                arp_timeout_s=float(data.get("arp_timeout_s", 1.0)),
                data_file=data.get("data_file", "data.json")
            )
    except (json.JSONDecodeError, ValueError):
        print(f"Warning: Could not parse config file {filepath}, using defaults.")
        return Config()
        
class DeviceResolver:
    def __init__(self, data_file: str) -> None:
        self.known_devices: Dict[str, str] = self.load_known_devices(data_file)

    @staticmethod
    def load_known_devices(filename: str) -> Dict[str, str]:
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                try:
                    raw_data: Any = json.load(f)
                    if isinstance(raw_data, dict):
                        return {
                            str(k).lower(): str(v) for k, v in raw_data.items()  # type: ignore
                            if isinstance(k, str) and isinstance(v, (str, int))  # optional sanity check
                        }
                except json.JSONDecodeError:
                    pass
        return {}

    def resolve_name(self, mac: str) -> str:
        return self.known_devices.get(mac.lower(), "Unknown")


class NetworkScanner:
    def __init__(self, config: Config, resolver: DeviceResolver) -> None:
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

        if retcode != 0:
            return None

        mac, arp_elapsed = self.arp_lookup(ip)
        if mac is None:
            return None

        name: str = self.resolver.resolve_name(mac)
        return NetworkDevice(
            ip=ip,
            mac=mac,
            name=name,
            ping_time_ms=round(ping_elapsed, 1),
            arp_time_ms=round(arp_elapsed, 1),
        )

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


if __name__ == "__main__":
    config = from_json_file("config.json")
    resolver = DeviceResolver(config.data_file)
    scanner = NetworkScanner(config, resolver)
    devices = scanner.scan_network()
