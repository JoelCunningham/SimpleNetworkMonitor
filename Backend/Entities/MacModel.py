from datetime import datetime, timezone
from typing import Optional, List

from sqlmodel import Field, Relationship

from Backend.Entities.BaseModel import BaseModel
from Backend.Entities.DeviceModel import Device


class Mac(BaseModel, table=True):
    address: str = Field(unique=True)

    last_ip: str
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    ping_time_ms: Optional[int] = Field(ge=0, default=None)
    arp_time_ms: Optional[int] = Field(ge=0, default=None)

    hostname: Optional[str] = Field(default=None)
    vendor: Optional[str] = Field(default=None)
    os_guess: Optional[str] = Field(default=None)
    ttl: Optional[int] = Field(default=None)
    
    device_id: Optional[int] = Field(default=None, foreign_key="device.id")
    device: Optional[Device] = Relationship(back_populates="macs")
    
    ports: List["Port"] = Relationship(back_populates="mac", cascade_delete=True)
    discoveries: List["Discovery"] = Relationship(back_populates="mac", cascade_delete=True)


from Backend.Entities.PortModel import Port
from Backend.Entities.DiscoveryModel import Discovery
