from pydantic import BaseModel


class DeviceRequest(BaseModel):
    name: str
    model: str
    category_id: int
    location_id: int
    owner_id: int
    mac_ids: list[int]