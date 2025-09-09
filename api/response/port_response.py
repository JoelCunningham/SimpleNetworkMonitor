from pydantic import BaseModel


class PortResponse(BaseModel):
    id: int
    port: int
    protocol: str 
    service: str
    banner: str | None
    state: str
    