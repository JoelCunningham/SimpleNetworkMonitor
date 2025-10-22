from typing import Protocol, Any


class CategoryServiceInterface(Protocol):
    """Interface for category CRUD operations."""

    def get_categories(self) -> list[Any]:
        ...

    def get_category(self, id: int) -> Any | None:
        ...

    def save_category(self, category: Any) -> Any:
        ...

    def delete_category(self, id: int) -> None:
        ...
