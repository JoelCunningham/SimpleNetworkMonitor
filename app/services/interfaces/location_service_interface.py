from typing import Protocol, Any


class LocationServiceInterface(Protocol):
    """Interface for location-related operations."""

    def get_locations(self) -> list[Any]:
        ...

    def get_location(self, id: int) -> Any | None:
        ...

    def save_location(self, location: Any) -> Any:
        ...

    def delete_location(self, id: int) -> None:
        ...
