from dataclasses import dataclass
from typing import Any


@dataclass
class KnownDevice:
    type: str
    owner: str
    location: str
    model: str
    
    @staticmethod
    def load(data: dict[str, Any]) -> "KnownDevice":
        return KnownDevice(
            type=str(data["type"]),
            owner=str(data["owner"]),
            location=str(data["location"]),
            model=str(data["model"]),
        )

    @staticmethod
    def hasDefaultOwner(device: "KnownDevice") -> bool:
        DEFAULT_DEVICE_OWNER: str = "Household"
        return device.owner == DEFAULT_DEVICE_OWNER
    
    def hasNoLocation(self) -> bool:
        DEFAULT_DEVICE_LOCATION: str = "None"
        return not self.location or self.location == DEFAULT_DEVICE_LOCATION