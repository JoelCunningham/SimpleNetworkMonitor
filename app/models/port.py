"""
Port model.

Represents an open network port on a MAC address.
"""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.mac import Mac

class Port(BaseModel, table=True):
    """Network port model."""    
    port: int = Field(nullable=False)
    protocol: str = Field(default="tcp", nullable=False, max_length=10)
    service: str | None = Field(default=None, max_length=100)
    banner: str | None = Field(default=None)
    state: str = Field(default="open", nullable=False, max_length=20)

    mac_id: int = Field(foreign_key="mac.id")
    mac: Optional["Mac"] = Relationship(back_populates="ports")
