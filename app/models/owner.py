"""
Owner model.

Represents device owners for organization.
"""

from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.base import BaseModel

if TYPE_CHECKING:
    from app.models.device import Device

class Owner(BaseModel, table=True):
    """Device owner model."""
    name: str = Field(nullable=False, unique=True, max_length=100)
    devices: list["Device"] = Relationship(back_populates="owner")
