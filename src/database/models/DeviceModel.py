from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship

from database.Database import BaseModel

if TYPE_CHECKING:
    from database.models.CategoryModel import Category
    from database.models.LocationModel import Location
    from database.models.MacModel import Mac
    from database.models.OwnerModel import Owner

class Device(BaseModel, table=True):
    id: int = Field(default=None, primary_key=True)
    model: str
    
    owner_id: Optional[int] = Field(default=None, foreign_key="owner.id")
    owner: Optional["Owner"] = Relationship(back_populates="devices")
    
    location_id: Optional[int] = Field(default=None, foreign_key="location.id")
    location: Optional["Location"] = Relationship(back_populates="devices")

    category_id: int = Field(default=None, foreign_key="category.id")
    category: "Category" = Relationship(back_populates="devices")
    
    macs: list["Mac"] = Relationship(back_populates="device")
