from pydantic import BaseModel


class OwnerSummary(BaseModel):
    id: int
    name: str
