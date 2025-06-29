"""Network ping and ARP resolution services."""
import platform
import subprocess
from typing import Optional, Tuple

from scapy.all import ARP, Ether, srp  # type: ignore
from scapy.packet import Packet

import Constants
import Exceptions
from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.INetworkScanning import INetworkPinger, IArpResolver
from Objects.Injectable import Injectable
from Utilities.Timer import Time, time_operation


class NetworkPinger(INetworkPinger, Injectable):
    """Service responsible for ping operations."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
        self._ping_cmd, self._ping_count_flag, self._ping_timeout_flag = self._setup_ping_command()
        
    def _setup_ping_command(self) -> Tuple[str, str, str]:
        """Setup ping command based on operating system."""
        system = platform.system()
        if system not in Constants.PING_COMMANDS:
            raise Exceptions.NetworkScanError(f"Unsupported operating system: {system}")
        
        cmd_info = Constants.PING_COMMANDS[system]
        return cmd_info["cmd"], cmd_info["count_flag"], cmd_info["timeout_flag"]
    
    def ping(self, ip_address: str) -> Optional[Tuple[bool, int, Optional[str]]]:
        """
        Ping an IP address.
        Returns: (success, response_time_ms, stdout) or None if error
        """
        network_settings = self._config_provider.get_network_settings()
        timeout_settings = self._config_provider.get_timeout_settings()
        
        ping_count = network_settings["ping_count"]
        ping_timeout_ms = timeout_settings["ping_timeout_ms"]
        
        # Adjust timeout value based on OS
        system = platform.system()
        if system == Constants.PLATFORM_WINDOWS:
            timeout_value = int(ping_timeout_ms)
        else:
            timeout_value = ping_timeout_ms / 1000
        
        ping_time = Time()
        
        try:
            with time_operation(ping_time):
                result = subprocess.run(
                    [
                        self._ping_cmd,
                        self._ping_count_flag, str(ping_count),
                        self._ping_timeout_flag, str(timeout_value),
                        ip_address
                    ],
                    capture_output=True,
                    text=True,
                    timeout=ping_timeout_ms / 1000 + 1
                )
            
            success = result.returncode == Constants.SUCCESSFUL_PING_EXIT_CODE
            return (success, int(ping_time.value), result.stdout if success else None)
            
        except (subprocess.TimeoutExpired, subprocess.SubprocessError) as e:
            print(f"Ping error for {ip_address}: {e}")
            return None


class ArpResolver(IArpResolver, Injectable):
    """Service responsible for ARP resolution."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._config_provider = config_provider
    
    def resolve_mac_address(self, ip_address: str) -> Optional[Tuple[str, int]]:
        """
        Resolve MAC address for IP.
        Returns: (mac_address, resolution_time_ms) or None if not found
        """
        timeout_settings = self._config_provider.get_timeout_settings()
        arp_timeout_ms = timeout_settings["arp_timeout_ms"]
        
        arp: Packet = ARP(pdst=ip_address)  # type: ignore
        ether: Packet = Ether(dst=Constants.BROADCAST_MAC_ADDRESS)  # type: ignore
        packet: Packet = ether / arp  # type: ignore

        arp_time = Time()
        with time_operation(arp_time):
            try:
                results = srp(packet, timeout=arp_timeout_ms/1000, verbose=0)[0]  # type: ignore
            except Exception as e:
                print(f"ARP lookup error for {ip_address}: {e}")
                return None

        if results:
            received_pkt = results[0][1]
            mac_address = getattr(received_pkt, "hwsrc", None)
            if mac_address and isinstance(mac_address, str):
                return (mac_address.lower(), int(arp_time.value))
        
        return None
