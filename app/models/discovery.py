"""
Discovery model.

Represents discovery information from network protocols.
"""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.mac import Mac
class Discovery(BaseModel, table=True):
    """Discovery information model."""    
    protocol: str = Field(default="unknown", nullable=False, max_length=50)
    device_name: str | None = Field(default=None, max_length=255)
    device_type: str | None = Field(default=None, max_length=100)
    manufacturer: str | None = Field(default=None, max_length=255)
    model: str | None = Field(default=None, max_length=255)

    mac_id: int = Field(foreign_key="mac.id")
    mac: Optional["Mac"] = Relationship(back_populates="discoveries")
