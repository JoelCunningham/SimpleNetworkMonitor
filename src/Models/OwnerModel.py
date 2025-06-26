from sqlmodel import Relationship

from Models.BaseModel import BaseModel
from Models.DeviceModel import Device


class Owner(BaseModel, table=True):
    name: str
    
    devices: list[Device] = Relationship(back_populates="owner")
