from typing import Protocol

from app.database.models import Category


class CategoryServiceInterface(Protocol):
    """Interface for handling category related operations."""

    def get_categories(self) -> list[Category]:
        """Return all categories from the database."""
        ...
