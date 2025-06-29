from typing import Optional

from sqlmodel import Field, Relationship

from Models.BaseModel import BaseModel


class Service(BaseModel, table=True):
    """Model for storing service information discovered through various protocols."""
    name: str = Field(index=True)
    port: Optional[int] = Field(default=None, ge=1, le=65535)
    protocol: Optional[str] = Field(default=None) 
    version: Optional[str] = Field(default=None)
    description: Optional[str] = Field(default=None)
    
    discovery_id: int = Field(foreign_key="discovery.id")
    discovery: Optional["Discovery"] = Relationship(back_populates="services")


from Models.DiscoveryModel import Discovery
