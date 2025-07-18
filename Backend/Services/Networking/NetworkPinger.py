import platform
import re
import subprocess

from Backend.Constants import PING_COMMANDS, PLATFORM_WINDOWS, SUCCESSFUL_PING_EXIT_CODE, TTL_REGEX
from Backend import Exceptions
from Backend.Objects.Injectable import Injectable
from Backend.Services.AppConfiguration import AppConfig
from Backend.Utilities.Timer import Time, time_operation


class NetworkPinger(Injectable):
    """Service responsible for ping operations."""
    
    def __init__(self, config: AppConfig) -> None:
        system = platform.system()
        if system not in PING_COMMANDS:
            raise Exceptions.NetworkScanError(f"Unsupported operating system: {system}")
        
        command = PING_COMMANDS[system]
    
        self._config = config
        self._ping_instruction = command.instruction
        self._ping_count_flag = command.count_flag
        self._ping_timeout_flag = command.timeout_flag
    
    def ping(self, ip_address: str) -> tuple[bool | None, int, str | None]:
        """Ping an IP address."""
        if platform.system() == PLATFORM_WINDOWS:
            timeout_value = self._config.timeout.ping_timeout_ms()
        else:
            timeout_value = self._config.timeout.ping_timeout_s()
        
        ping_time = Time()
        
        try:
            with time_operation(ping_time):
                result = subprocess.run(
                    [
                        self._ping_instruction,
                        self._ping_count_flag, str(self._config.network.ping_count()),
                        self._ping_timeout_flag, str(timeout_value),
                        ip_address
                    ],
                    capture_output=True,
                    text=True,
                    timeout=self._config.timeout.ping_timeout_s() + 1
                )
            
            success = result.returncode == SUCCESSFUL_PING_EXIT_CODE
            return (success, int(ping_time.value), result.stdout if success else None)
            
        except (subprocess.TimeoutExpired) as e:
           return None, 0, None
       
        except (subprocess.SubprocessError) as e:
            print(f"WARN ping error for {ip_address}: {e}")
            return None, 0, None

    def get_ttl_from_ping_result(self, ping_result: str) -> int | None:
        """Extract TTL value from ping output."""
        try:
            ttl_match = re.search(TTL_REGEX, ping_result)
            if ttl_match:
                return int(ttl_match.group(1))
        except (ValueError, AttributeError):
            pass
        return None