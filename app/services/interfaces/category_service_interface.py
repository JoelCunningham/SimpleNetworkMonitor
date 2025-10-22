from typing import Protocol

from app.models.category import Category


class CategoryServiceInterface(Protocol):
    """Interface for handling category related operations."""

    def get_categories(self) -> list[Category]:
        """Return all categories from the database."""
        ...
