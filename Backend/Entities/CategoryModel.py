from typing import TYPE_CHECKING

from sqlmodel import Relationship

from Backend.Entities.BaseModel import BaseModel

if TYPE_CHECKING:
    from Backend.Entities.DeviceModel import Device


class Category(BaseModel, table=True):
    name: str
    
    devices: list["Device"] = Relationship(back_populates="category")
