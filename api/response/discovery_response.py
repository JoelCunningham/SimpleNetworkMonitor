from pydantic import BaseModel


class DiscoveryResponse(BaseModel):
    id: int
    protocol: str
    device_name: str | None
    device_type: str | None
    manufacturer: str | None
    model: str | None
