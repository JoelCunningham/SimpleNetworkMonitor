import platform
import subprocess
from typing import Optional, Tuple

from Backend.Constants import PING_COMMANDS, PLATFORM_WINDOWS, SUCCESSFUL_PING_EXIT_CODE
from Backend import Exceptions
from Backend.Objects.Injectable import Injectable
from Backend.Services.AppConfiguration import AppConfig
from Backend.Utilities.Timer import Time, time_operation


class NetworkPinger(Injectable):
    """Service responsible for ping operations."""
    
    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._ping_cmd, self._ping_count_flag, self._ping_timeout_flag = self._setup_ping_command()
        
    def _setup_ping_command(self) -> Tuple[str, str, str]:
        """Setup ping command based on operating system."""
        system = platform.system()
        if system not in PING_COMMANDS:
            raise Exceptions.NetworkScanError(f"Unsupported operating system: {system}")
        
        cmd_info = PING_COMMANDS[system]
        return cmd_info["cmd"], cmd_info["count_flag"], cmd_info["timeout_flag"]
    
    def ping(self, ip_address: str) -> Tuple[Optional[bool], int, Optional[str]]:
        """
        Ping an IP address.
        Returns: (success, response_time_ms, stdout) or None if error
        """
        system = platform.system()
        if system == PLATFORM_WINDOWS:
            timeout_value = self._config.timeout.ping_timeout_ms()
        else:
            timeout_value = self._config.timeout.ping_timeout_s()
        
        ping_time = Time()
        
        try:
            with time_operation(ping_time):
                result = subprocess.run(
                    [
                        self._ping_cmd,
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

