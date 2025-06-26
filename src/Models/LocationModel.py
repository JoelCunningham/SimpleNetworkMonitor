from sqlmodel import Relationship

from Database import BaseModel
from Models.DeviceModel import Device

class Location(BaseModel, table=True):
    name: str
    
    devices: list[Device] = Relationship(back_populates="location")
