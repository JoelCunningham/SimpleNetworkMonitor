import platform
import re
import socket
import subprocess

from app import config
from app.common.constants import *
from app.common.objects import PingCommand
from app.common.utilities import Time, time_operation
from app.services.interfaces import PingServiceInterface


class PingService(PingServiceInterface):
    """Service responsible for ping operations."""

    def __init__(self) -> None:
        PING_COMMANDS = {
            PLATFORM_WINDOWS: PingCommand("ping", "-n", "-w"),
            PLATFORM_LINUX: PingCommand("ping", "-c", "-W"),
            PLATFORM_MACOS: PingCommand("ping", "-c", "-W"),
        }
        
        system = platform.system()
        if system not in PING_COMMANDS:
            raise Exception(f"Unsupported operating system: {system}")
    
        self._ping_count_flag = PING_COMMANDS[system].count_flag
        self._ping_instruction = PING_COMMANDS[system].instruction
        self._ping_timeout_flag = PING_COMMANDS[system].timeout_flag
    
    def ping(self, ip_address: str) -> tuple[bool | None, int, str | None]:
        ping_timeout_ms = config.ping_timeout_ms if config else 2000
        ping_count = config.ping_count if config else 3
        ping_time = Time()
        
        if platform.system() == PLATFORM_WINDOWS:
            timeout_value = ping_timeout_ms
        else:
            timeout_value = ping_timeout_ms // 1000
        
        try:
            with time_operation(ping_time):
                result = subprocess.run(
                    [
                        self._ping_instruction,
                        self._ping_count_flag, str(ping_count),
                        self._ping_timeout_flag, str(timeout_value),
                        ip_address
                    ],
                    capture_output=True,
                    text=True,
                    timeout=(ping_timeout_ms // 1000) + 1
                )
            
            success = result.returncode == SUCCESSFUL_PING_EXIT_CODE
            return (success, int(ping_time.value), result.stdout if success else None)
            
        except subprocess.TimeoutExpired:
            return None, 0, None

        except subprocess.SubprocessError as e:
            print(f"WARN ping error for {ip_address}: {e}")
            return None, 0, None

    def get_hostname(self, ip_address: str) -> str | None:
        try:
            timeout = (config.hostname_timeout_ms if config else 1000) / 1000
            socket.setdefaulttimeout(timeout)
            hostname, _, _ = socket.gethostbyaddr(ip_address)
            return hostname
        except (socket.herror, socket.gaierror, socket.timeout):
            return None
        finally:
            socket.setdefaulttimeout(None)

    def get_ttl_from_ping(self, ping_result: str) -> int | None:
        try:
            ttl_match = re.search(TTL_REGEX, ping_result)
            if ttl_match:
                return int(ttl_match.group(1))
        except (ValueError, AttributeError):
            pass
        return None

    def get_os_from_ttl(self, ttl: int) -> str:
        if ttl in TTL_OS_MAPPING:
            return TTL_OS_MAPPING[ttl]
        
        # Check for TTL values that might have passed through routers
        for expected_ttl, os_name in TTL_OS_MAPPING.items():
            if expected_ttl - 10 <= ttl <= expected_ttl:
                return ROUTER_TTL_TEMPLATE.format(os_name=os_name)
        
        return UNKNOWN_OS_TEMPLATE.format(ttl=ttl)