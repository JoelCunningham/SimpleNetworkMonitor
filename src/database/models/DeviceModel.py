from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship

from database.Database import BaseModel

if TYPE_CHECKING:
    from database.models.CategoryModel import Category
    from database.models.LocationModel import Location
    from database.models.MacModel import Mac
    from database.models.OwnerModel import Owner

class Device(BaseModel, table=True):
    model: Optional[str] = Field(default=None) 
    
    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")
    owner: Optional["Owner"] = Relationship(back_populates="devices")
    
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    location: Optional["Location"] = Relationship(back_populates="devices")

    category_id: int = Field(foreign_key="category.id") 
    category: "Category" = Relationship(back_populates="devices")
    
    macs: List["Mac"] = Relationship(back_populates="device")
