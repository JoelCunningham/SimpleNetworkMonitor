from pydantic import BaseModel


class OwnerRequest(BaseModel):
    name: str
    device_ids: list[int]