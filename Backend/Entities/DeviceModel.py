from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from Backend.Constants import UNKNOWN_DEVICE_NAME
from Backend.Entities.BaseModel import BaseModel

if TYPE_CHECKING:
    from Backend.Entities.CategoryModel import Category
    from Backend.Entities.LocationModel import Location
    from Backend.Entities.MacModel import Mac
    from Backend.Entities.OwnerModel import Owner


class Device(BaseModel, table=True):
    model: str | None = Field(default=None) 
    
    owner_id: int | None = Field(default=None, foreign_key="owner.id")
    owner: "Owner" = Relationship(back_populates="devices")
    
    location_id: int | None = Field(default=None, foreign_key="location.id")
    location: "Location" = Relationship(back_populates="devices")

    category_id: int = Field(foreign_key="category.id") 
    category: "Category" = Relationship(back_populates="devices")
    
    macs: list["Mac"] = Relationship(back_populates="device")
   
    @property
    def name(self) -> str:
        device_name = ""
        
        device_name += self.owner.name + "'s " if self.owner else ""
        device_name += self.location.name + " " if self.location else ""
        device_name += self.category.name if self.category else ""
    
        return device_name.strip() or UNKNOWN_DEVICE_NAME
        
    @property
    def primary_mac(self) -> "Mac | None":
        if not self.macs:
            return None
        return max(self.macs, key=lambda mac: mac.last_seen or 0)
    