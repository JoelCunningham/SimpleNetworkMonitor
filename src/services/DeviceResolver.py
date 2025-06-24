import json
import os
from typing import Any, Dict, Optional

from objects.KnownDevice import KnownDevice


class DeviceResolver:
    def __init__(self, data_file: str) -> None:
        self.known_devices: Dict[str, KnownDevice] = self.load_known_devices(data_file)

    def resolve(self, mac: str) -> Optional[KnownDevice]:
        return self.known_devices.get(mac.lower())

    @staticmethod
    def load_known_devices(filename: str) -> Dict[str, KnownDevice]:
        ENCODING = "utf-8"
        mac_lookup: Dict[str, KnownDevice] = {}

        if os.path.exists(filename):
            with open(filename, "r", encoding=ENCODING) as f:
                try:
                    raw_data: Dict[str, Any] = json.load(f)

                    for _id, data in raw_data.items():
                        if "macs" not in data or not isinstance(data["macs"], list):
                            continue

                        known_device = KnownDevice.load(data)

                        for mac in data["macs"]:
                            if isinstance(mac, str):
                                mac_lookup[mac.lower()] = known_device

                except (json.JSONDecodeError, TypeError):
                    pass

        return mac_lookup
