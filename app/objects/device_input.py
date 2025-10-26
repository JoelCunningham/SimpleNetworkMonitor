from pydantic import BaseModel


class DeviceInput(BaseModel):
    name: str | None
    model: str | None
    category_id: int
    location_id: int | None
    owner_id: int | None
    mac_ids: list[int]