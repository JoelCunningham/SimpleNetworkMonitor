from pydantic import BaseModel

from app.api.response.device_summary import DeviceSummary


class OwnerResponse(BaseModel):   
    id: int
    name: str
    devices: list[DeviceSummary]