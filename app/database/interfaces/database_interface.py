from typing import Protocol, TypeVar

from app.database.interfaces import QueryInterface
from app.database.models import BaseModel

T = TypeVar("T", bound=BaseModel)

class DatabaseInterface(Protocol):
    """Interface for handling category related operations."""

    def select(self, model: type[T]) -> QueryInterface[T]:
        """Initiate a query for the specified model."""
        ...
        
    def create(self, instance: BaseModel) -> None:
        """Insert a new record into the database."""
        ...
        
    def update(self, instance: BaseModel) -> None:
        """Update an existing record in the database."""
        ...
        
    def delete(self, instance: BaseModel) -> None:
        """Delete a record from the database."""
        ...
