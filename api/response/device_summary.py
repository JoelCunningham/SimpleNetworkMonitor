from pydantic import BaseModel

from api.response.category_response import CategoryResponse
from api.response.location_response import LocationResponse
from api.response.mac_response import MacResponse


class DeviceSummary(BaseModel):
    id: int
    name: str | None
    model: str | None
    category: CategoryResponse
    location: LocationResponse | None
    macs: list[MacResponse]
    primary_mac: MacResponse
