from sqlmodel import Field, Relationship

from database.Database import BaseModel
from database.models.DeviceModel import Device


class Owner(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    
    devices: list[Device] = Relationship(back_populates="owner")
