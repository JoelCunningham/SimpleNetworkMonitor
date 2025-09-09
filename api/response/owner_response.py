from pydantic import BaseModel

class OwnerResponse(BaseModel):   
    class Device(BaseModel):
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
        name: str
        model: str
        category: Category
        location: Location
        owner: Owner
        macs: list[Mac]
        
    id: int
    name: str
    devices: list[Device] = []
