"""
Device model.

Represents network devices discovered during scans.
"""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.category import Category
    from app.models.location import Location
    from app.models.mac import Mac
    from app.models.owner import Owner

class Device(BaseModel, table=True):
    """Device model representing a network device.""" 
    name: str | None = Field(default=None, unique=True, max_length=200)
    model: str | None = Field(default=None, max_length=200)

    category_id: int | None = Field(default=None, foreign_key="category.id")
    location_id: int | None = Field(default=None, foreign_key="location.id")
    owner_id: int | None = Field(default=None, foreign_key="owner.id")

    category: Optional["Category"] = Relationship(back_populates="devices")
    location: Optional["Location"] = Relationship(back_populates="devices")
    owner: Optional["Owner"] = Relationship(back_populates="devices")
    macs: list["Mac"] = Relationship(back_populates="device")

    @property
    def primary_mac(self) -> Optional["Mac"]:
        """Get the primary MAC address (most recently seen)."""
        if not self.macs:
            return None
        return max(self.macs, key=lambda mac: mac.last_seen or 0)
