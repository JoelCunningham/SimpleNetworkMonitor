import json
import os
from typing import Any, Dict


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
                            if isinstance(k, str) and isinstance(v, (str, int)) 
                        }
                except json.JSONDecodeError:
                    pass
        return {}

    def resolve_name(self, mac: str) -> str:
        return self.known_devices.get(mac.lower(), "Unknown")
