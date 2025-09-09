"""
MAC address model.

Represents a network MAC address with associated network information.
"""


from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Column, DateTime, Field, Relationship, func

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.device import Device
    from app.models.discovery import Discovery
    from app.models.port import Port
    
class Mac(BaseModel, table=True):
    """MAC address model."""
    address: str = Field(nullable=False, unique=True, max_length=17)
    last_ip: str = Field(nullable=False, max_length=45)
    last_seen: datetime = Field(sa_column=Column(DateTime, default=func.now()))

    ping_time_ms: int | None = Field(default=None)
    arp_time_ms: int | None = Field(default=None)

    hostname: str | None = Field(default=None, max_length=255)
    vendor: str | None = Field(default=None, max_length=255)
    os_guess: str | None = Field(default=None, max_length=255)
    ttl: int | None = Field(default=None)

    device_id: int | None = Field(default=None, foreign_key="device.id")

    device: Optional["Device"] = Relationship(back_populates="macs")
    ports: list["Port"] = Relationship(back_populates="mac")
    discoveries: list["Discovery"] = Relationship(back_populates="mac")
