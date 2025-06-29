from typing import Optional, List

from sqlmodel import Field, Relationship

from Models.BaseModel import BaseModel


class Discovery(BaseModel, table=True):
    """Model for storing discovery information related to a MAC address."""
    protocol: str = Field(default="unknown")
    device_name: Optional[str] = Field(default=None)
    device_type: Optional[str] = Field(default=None)
    manufacturer: Optional[str] = Field(default=None)
    model: Optional[str] = Field(default=None)
    
    mac_id: int = Field(foreign_key="mac.id")
    mac: Optional["Mac"] = Relationship(back_populates="discoveries")
    
    services: List["Service"] = Relationship(back_populates="discovery", cascade_delete=True)


from Models.MacModel import Mac
from Models.ServiceModel import Service
