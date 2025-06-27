from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship

from Models.BaseModel import BaseModel
from Models.DeviceModel import Device


class Mac(BaseModel, table=True):
    address: str = Field(unique=True)

    ping_time_ms: int = Field(ge=0)
    arp_time_ms: int = Field(ge=0)

    last_ip: str
    last_seen: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    hostname: Optional[str] = Field(default=None)
    vendor: Optional[str] = Field(default=None)
    os_guess: Optional[str] = Field(default=None)
    ttl: Optional[int] = Field(default=None)

    device_id: Optional[int] = Field(default=None, foreign_key="device.id")
    device: Optional[Device] = Relationship(back_populates="macs")
