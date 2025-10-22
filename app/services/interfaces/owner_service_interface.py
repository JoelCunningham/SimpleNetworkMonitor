from typing import Protocol, Any


class OwnerServiceInterface(Protocol):
    """Interface for owner-related operations."""

    def get_all_owners(self) -> list[Any]:
        ...

    def get_owner(self, id: int) -> Any | None:
        ...

    def save_owner(self, owner: Any) -> Any:
        ...

    def delete_owner(self, id: int) -> None:
        ...
