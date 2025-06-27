import platform
import subprocess
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet

import Constants
import Exceptions
from Objects.AddressData import AddressData
from Objects.Injectable import Injectable
from Services.AppConfig import AppConfig
from Services.DeviceEnrichmentService import DeviceEnrichmentService
from Utilities.Timer import Time, time_operation


class NetworkScanner(Injectable):
    _config: AppConfig
    _enrichment_service: DeviceEnrichmentService
    
    _ping_cmd: str
    _ping_count_flag: str
    _ping_timeout_flag: str
    _ping_timeout_value: float
    
    def __init__(self, config: AppConfig, enrichment_service: DeviceEnrichmentService) -> None:
        self._config = config
        self._enrichment_service = enrichment_service
        
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
                result = subprocess.run(
                    [
                        self._ping_cmd,
                        self._ping_count_flag, str(self._config.ping_count),
                        self._ping_timeout_flag, str(self._ping_timeout_value),
                        ip_address
                    ],
                    capture_output=True,
                    text=True,
                    timeout=self._config.ping_timeout_ms / 1000 + 1
                )                                                      
            except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
                print(f"Ping error for {ip_address}: {e}")
                return None
                 
        if result.returncode != Constants.SUCCESSFUL_PING_EXIT_CODE:
            return None
      
        mac: Optional[str] = None
        ttl: Optional[int] = None
        arp_time: Time = Time()
        hostname: Optional[str] = None
        mac_vendor: Optional[str] = None
        os_guess: Optional[str] = None
      
        if self._config.mac_resolution and ip_address:
            mac, arp_time = self._lookup_arp(ip_address)
          
        if self._config.hostname_resolution and ip_address:
            hostname = self._enrichment_service.resolve_hostname(ip_address)
        
        if self._config.mac_vendor_lookup and mac:
            mac_vendor = self._enrichment_service.get_mac_vendor(mac)
            
        if self._config.os_detection and result.stdout:  
            ttl = self._extract_ttl_from_ping_output(result.stdout) 
            if ttl:
                os_guess = self._enrichment_service.guess_os_from_ttl(ttl)

        return AddressData(
            mac_address=mac, 
            ip_address=ip_address, 
            ping_time_ms=int(ping_time.value), 
            arp_time_ms=int(arp_time.value),
            hostname=hostname,
            mac_vendor=mac_vendor,
            os_guess=os_guess,
            ttl=ttl
        )

    def _lookup_arp(self, ip: str) -> Tuple[Optional[str], Time]:
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

    def _extract_ttl_from_ping_output(self, ping_output: str) -> Optional[int]:
        try:
            ttl_match = re.search(Constants.TTL_REGEX, ping_output)
            if ttl_match:
                return int(ttl_match.group(1))
        except (ValueError, AttributeError):
            pass
        return None
