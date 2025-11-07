from typing import Any, Generic, Protocol, TypeVar

from app.database.models import BaseModel

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=Any)

class QueryInterface(Generic[T], Protocol):
    """Interface for handling query related operations."""

    def where(self, condition: Any) -> "QueryInterface[T]":
        """Add a WHERE condition to the query."""
        ...

    def where_in(self, column: U, values: list[U]) -> "QueryInterface[T]":
        """Add a WHERE IN condition to the query."""
        ...
        
    def order_by(self, *criteria: Any) -> "QueryInterface[T]":
        """Add ORDER BY criteria to the query."""
        ...
        
    def all(self) -> list[T]:
        """Execute the query and return all results."""
        ...
        
    def first(self) -> T | None:
        """Execute the query and return the first result."""
        ...
        
    def by_id(self, id: int) -> T | None:
        """Execute the query and return a single result by ID."""
        ...