
"""
Base model class with common functionality (SQLModel version).
"""
from datetime import datetime

from sqlmodel import Field, SQLModel


class BaseModel(SQLModel):
    id: int = Field(default=None, primary_key=True, index=True)
    deleted: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(), nullable=False)
