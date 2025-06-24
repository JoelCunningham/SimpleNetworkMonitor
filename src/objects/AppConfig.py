import json
import os
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AppConfig:
    subnet: str
    min_ip: int
    max_ip: int
    max_threads: int
    ping_count: int
    ping_timeout_ms: int
    arp_timeout_ms: int

    @staticmethod
    def load(filepath: str) -> "AppConfig":
        ENCODING = "utf-8"
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"AppConfig file {filepath} does not exist.")
        try:
            with open(filepath, "r", encoding=ENCODING) as file:
                data: Dict[str, Any] = json.load(file)
                
                return AppConfig(
                    subnet=str(data["subnet"]),
                    min_ip=int(data["min_ip"]),
                    max_ip=int(data["max_ip"]),
                    max_threads=int(data["max_threads"]),
                    ping_count=int(data["ping_count"]),
                    ping_timeout_ms=int(data["ping_timeout_ms"]),
                    arp_timeout_ms=int(data["arp_timeout_ms"]),
                )
        except (json.JSONDecodeError, ValueError):
            raise ValueError(f"Invalid configuration in {filepath}. Please check the format.")