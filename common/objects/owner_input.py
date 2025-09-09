from dataclasses import dataclass

@dataclass
class OwnerInput:
    name: str
    device_ids: list[int] 