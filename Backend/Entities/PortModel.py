from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from Backend.Entities.BaseModel import BaseModel

if TYPE_CHECKING:
    from Backend.Entities.MacModel import Mac


class Port(BaseModel, table=True):
    port: int = Field(ge=1, le=65535)
    protocol: str = Field(default="tcp")
    service: str | None = Field(default=None)
    banner: str | None = Field(default=None)
    state: str = Field(default="open")
    
    mac_id: int = Field(foreign_key="mac.id")
    mac: "Mac" = Relationship(back_populates="ports")
