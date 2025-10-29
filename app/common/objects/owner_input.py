from pydantic import BaseModel


class OwnerInput(BaseModel):
    name: str
    device_ids: list[int]
    