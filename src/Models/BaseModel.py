from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True)
    deleted: bool = False