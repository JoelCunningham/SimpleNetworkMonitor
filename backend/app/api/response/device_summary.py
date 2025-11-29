from pydantic import BaseModel

from app.api.response.category_response import CategoryResponse
from app.api.response.location_response import LocationResponse
from app.api.response.mac_response import MacResponse


class DeviceSummary(BaseModel):
    id: int
    name: str | None
    model: str | None
    category: CategoryResponse
    location: LocationResponse | None
    macs: list[MacResponse]
    primary_mac: MacResponse
