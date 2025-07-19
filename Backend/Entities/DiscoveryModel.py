from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from Backend.Entities.BaseModel import BaseModel

if TYPE_CHECKING:
    from Backend.Entities.MacModel import Mac
    from Backend.Entities.ServiceModel import Service


class Discovery(BaseModel, table=True):
    """Model for storing discovery information related to a MAC address."""
    protocol: str = Field(default="unknown")
    device_name: str | None = Field(default=None)
    device_type: str | None = Field(default=None)
    manufacturer: str | None = Field(default=None)
    model: str | None = Field(default=None)
    
    mac_id: int = Field(foreign_key="mac.id")
    mac: "Mac" = Relationship(back_populates="discoveries")
    
    services: list["Service"] = Relationship(back_populates="discovery", cascade_delete=True)
