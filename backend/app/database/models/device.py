"""
Device model.

Represents network devices discovered during scans.
"""

from typing import TYPE_CHECKING, Optional

from sqlmodel import Field

from app.database.models import BaseModel
from app.database.relation import Relation

if TYPE_CHECKING:
    from app.database.models import Category, Location, Mac, Owner

class Device(BaseModel, table=True):
    """Device model representing a network device.""" 
    name: str | None = Field(default=None, unique=True, max_length=200)
    model: str | None = Field(default=None, max_length=200)

    category_id: int | None = Field(default=None, foreign_key="category.id")
    location_id: int | None = Field(default=None, foreign_key="location.id")
    owner_id: int | None = Field(default=None, foreign_key="owner.id")

    category: Optional["Category"] = Relation().backward("Device", "Category")
    location: Optional["Location"] = Relation().backward("Device", "Location")
    owner: Optional["Owner"] = Relation().backward("Device", "Owner")
    macs: list["Mac"] = Relation().forward("Device", "Mac")

    @property
    def primary_mac(self) -> Optional["Mac"]:
        """Get the primary MAC address (most recently seen)."""
        if not self.macs:
            return None
        return max(self.macs, key=lambda mac: mac.last_seen or 0)
