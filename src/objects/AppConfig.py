import json
import os
from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class AppConfig:
    subnet: str
    min_ip: str
    max_ip: str
    max_threads: int
    ping_count: int
    ping_timeout_ms: int
    arp_timeout_s: float
    data_file: str

    @staticmethod
    def load(filepath: str) -> "AppConfig":
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"AppConfig file {filepath} does not exist.")
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                data: Dict[str, Any] = json.load(file)
                
                return AppConfig(
                    subnet=str(data["subnet"]),
                    min_ip=str(data["min_ip"]),
                    max_ip=str(data["max_ip"]),
                    max_threads=int(data["max_threads"]),
                    ping_count=int(data["ping_count"]),
                    ping_timeout_ms=int(data["ping_timeout_ms"]),
                    arp_timeout_s=float(data["arp_timeout_s"]),
                    data_file=str(data["data_file"])
                )
        except (json.JSONDecodeError, ValueError):
            raise ValueError(f"Invalid configuration in {filepath}. Please check the format.")