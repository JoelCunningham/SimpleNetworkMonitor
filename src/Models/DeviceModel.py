from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from Database import BaseModel

if TYPE_CHECKING:
    from Models.CategoryModel import Category
    from Models.LocationModel import Location
    from Models.MacModel import Mac
    from Models.OwnerModel import Owner

class Device(BaseModel, table=True):
    model: Optional[str] = Field(default=None) 
    
    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")
    owner: Optional["Owner"] = Relationship(back_populates="devices")
    
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    location: Optional["Location"] = Relationship(back_populates="devices")

    category_id: int = Field(foreign_key="category.id") 
    category: "Category" = Relationship(back_populates="devices")
    
    macs: List["Mac"] = Relationship(back_populates="device")
