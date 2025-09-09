from pydantic import BaseModel


class DeviceResponse(BaseModel):
    class Category(BaseModel):
        id: int
        name: str

    class Location(BaseModel):
        id: int
        name: str

    class Owner(BaseModel):
        id: int
        name: str

    class Mac(BaseModel):
        id: int
        address: str

    id: int
    name: str | None
    model: str | None
    category: Category
    location: Location | None
    owner: Owner | None
    macs: list[Mac]
