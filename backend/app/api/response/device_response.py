from pydantic import BaseModel

from app.api.response.category_response import CategoryResponse
from app.api.response.location_response import LocationResponse
from app.api.response.mac_response import MacResponse
from app.api.response.owner_summary import OwnerSummary


class DeviceResponse(BaseModel):
    id: int | None
    name: str | None
    model: str | None
    category: CategoryResponse | None
    location: LocationResponse | None
    owner: OwnerSummary | None
    macs: list[MacResponse]
    primary_mac: MacResponse
