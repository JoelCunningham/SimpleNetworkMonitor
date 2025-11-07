"""
Category model.

Represents device categories for organization.
"""
from typing import TYPE_CHECKING

from sqlmodel import Field

from app.database.models import BaseModel
from app.database.relation import Relation

if TYPE_CHECKING:
    from app.database.models import Device

class Category(BaseModel, table=True):
    """Device category model."""    
    name: str = Field(nullable=False, unique=True, max_length=100)
    devices: list["Device"] = Relation().forward("Category", "Device")
