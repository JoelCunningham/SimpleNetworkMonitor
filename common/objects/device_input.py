from dataclasses import dataclass

@dataclass
class DeviceInput:
    name: str
    model: str
    category_id: int
    location_id: int
    owner_id: int
    mac_ids: list[int]