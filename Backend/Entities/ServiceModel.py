from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from Backend.Entities.BaseModel import BaseModel

if TYPE_CHECKING:
    from Backend.Entities.DiscoveryModel import Discovery


class Service(BaseModel, table=True):
    """Model for storing service information discovered through various protocols."""
    name: str = Field(index=True)
    port: int | None = Field(default=None, ge=1, le=65535)
    protocol: str | None = Field(default=None) 
    version: str | None = Field(default=None)
    description: str | None = Field(default=None)
    
    discovery_id: int = Field(foreign_key="discovery.id")
    discovery: "Discovery" = Relationship(back_populates="services")
