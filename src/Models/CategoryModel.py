from sqlmodel import Field, Relationship

from Database import BaseModel
from Models.DeviceModel import Device


class Category(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    
    devices: list[Device] = Relationship(back_populates="category")
