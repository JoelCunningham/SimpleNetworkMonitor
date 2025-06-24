from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, Relationship

from database.Database import BaseModel
from database.models.DeviceModel import Device


class Mac(BaseModel, table=True):
    address: str = Field(primary_key=True)

    ping_time_ms: int
    arp_time_ms: int

    last_ip: str
    last_seen: datetime = Field(default=datetime.now(timezone.utc))

    device_id: int = Field(default=None, foreign_key="device.id")
    device: Optional[Device] = Relationship(back_populates="macs")
