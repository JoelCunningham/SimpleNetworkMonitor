from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from Backend.Entities.BaseModel import BaseModel

if TYPE_CHECKING:
    from Backend.Entities.DeviceModel import Device
    from Backend.Entities.DiscoveryModel import Discovery
    from Backend.Entities.PortModel import Port


class Mac(BaseModel, table=True):
    address: str = Field(unique=True)

    last_ip: str
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    ping_time_ms: int | None = Field(ge=0, default=None)
    arp_time_ms: int | None = Field(ge=0, default=None)

    hostname: str | None = Field(default=None)
    vendor: str | None = Field(default=None)
    os_guess: str | None = Field(default=None)
    ttl: int | None = Field(default=None)
    
    device_id: int | None = Field(default=None, foreign_key="device.id")
    device: "Device" = Relationship(back_populates="macs")
    
    ports: list["Port"] = Relationship(back_populates="mac", cascade_delete=True)
    discoveries: list["Discovery"] = Relationship(back_populates="mac", cascade_delete=True)
