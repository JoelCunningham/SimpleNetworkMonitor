from typing import Optional

from sqlmodel import Field, Relationship

from Models.BaseModel import BaseModel


class Port(BaseModel, table=True):
    port: int = Field(ge=1, le=65535)
    protocol: str = Field(default="tcp")
    service: Optional[str] = Field(default=None)
    banner: Optional[str] = Field(default=None)
    state: str = Field(default="open")
    
    mac_id: int = Field(foreign_key="mac.id")
    mac: Optional["Mac"] = Relationship(back_populates="ports")


from Models.MacModel import Mac
