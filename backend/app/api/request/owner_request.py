from pydantic import BaseModel

from app.common.objects.owner_input import OwnerInput


class OwnerRequest(BaseModel):
    name: str
    device_ids: list[int]

    def toOwnerInput(self) -> OwnerInput:
        return OwnerInput(
            name=self.name,
            device_ids=self.device_ids,
        )