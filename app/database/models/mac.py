"""
MAC address model.

Represents a network MAC address with associated network information.
"""


from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field

from app.database.models import BaseModel
from app.database.relation import Relation

if TYPE_CHECKING:
    from app.database.models import Device, Discovery, Port
    
class Mac(BaseModel, table=True):
    """MAC address model."""
    address: str = Field(nullable=False, unique=True, max_length=17)
    last_ip: str = Field(nullable=False, max_length=45)
    last_seen: datetime = Field(nullable=False)

    ping_time_ms: int | None = Field(default=None)
    arp_time_ms: int | None = Field(default=None)

    hostname: str | None = Field(default=None, max_length=255)
    vendor: str | None = Field(default=None, max_length=255)
    os_guess: str | None = Field(default=None, max_length=255)
    ttl: int | None = Field(default=None)

    device_id: int | None = Field(default=None, foreign_key="device.id")

    device: Optional["Device"] = Relation().backward("Mac", "Device")
    ports: list["Port"] = Relation().forward("Mac", "Port")
    discoveries: list["Discovery"] = Relation().forward("Mac", "Discovery")
