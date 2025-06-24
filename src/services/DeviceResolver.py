import json
import os
from typing import Any, Dict, Optional

from objects.KnownDevice import KnownDevice


class DeviceResolver:
    def __init__(self, data_file: str) -> None:
        self.known_devices: Dict[str, KnownDevice] = self.load_known_devices(data_file)

    def resolve(self, mac: str) -> Optional[KnownDevice]:
        if mac not in self.known_devices:
            return None
        return self.known_devices[mac]

    @staticmethod
    def load_known_devices(filename: str) -> Dict[str, KnownDevice]:
        ENCODING = "utf-8"
        
        if os.path.exists(filename):
            with open(filename, "r", encoding=ENCODING) as f:
                try:
                    raw_data: Dict[str, Any] = json.load(f)
                    known_devices: Dict[str, KnownDevice] = {}
                    
                    for mac, data in raw_data.items():
                        known_device = KnownDevice.load(data)
                        known_devices[mac] = known_device
                    return known_devices
                
                except (json.JSONDecodeError, TypeError):
                    pass
        return {}
