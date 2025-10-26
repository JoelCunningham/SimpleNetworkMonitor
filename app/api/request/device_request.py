from pydantic import BaseModel

from app.objects.device_input import DeviceInput


class DeviceRequest(BaseModel):
    name: str | None
    model: str | None
    category_id: int
    location_id: int | None
    owner_id: int | None
    mac_ids: list[int]
    
    def toDeviceInput(self) -> DeviceInput:
        return DeviceInput(
            name=self.name,
            model=self.model,
            category_id=self.category_id,
            location_id=self.location_id,
            owner_id=self.owner_id,
            mac_ids=self.mac_ids,
        )