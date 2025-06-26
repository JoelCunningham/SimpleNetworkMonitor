from sqlmodel import Relationship

from database.Database import BaseModel
from database.models.DeviceModel import Device

class Location(BaseModel, table=True):
    name: str
    
    devices: list[Device] = Relationship(back_populates="location")
