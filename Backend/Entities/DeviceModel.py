from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from Backend.Entities.BaseModel import BaseModel

if TYPE_CHECKING:
    from Backend.Entities.CategoryModel import Category
    from Backend.Entities.LocationModel import Location
    from Backend.Entities.MacModel import Mac
    from Backend.Entities.OwnerModel import Owner

class Device(BaseModel, table=True):
    model: Optional[str] = Field(default=None) 
    
    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")
    owner: Optional["Owner"] = Relationship(back_populates="devices")
    
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    location: Optional["Location"] = Relationship(back_populates="devices")

    category_id: int = Field(foreign_key="category.id") 
    category: "Category" = Relationship(back_populates="devices")
    
    macs: List["Mac"] = Relationship(back_populates="device")
