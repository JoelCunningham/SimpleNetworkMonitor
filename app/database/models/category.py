"""
Category model.

Represents device categories for organization.
"""
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.database.models import BaseModel

if TYPE_CHECKING:
    from app.database.models import Device

class Category(BaseModel, table=True):
    """Device category model."""    
    name: str = Field(nullable=False, unique=True, max_length=100)
    devices: list["Device"] = Relationship(back_populates="category")
