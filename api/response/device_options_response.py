from pydantic import BaseModel


class DeviceOptionsResponse(BaseModel):
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

    categories: list[Category]
    locations: list[Location]
    owners: list[Owner]
