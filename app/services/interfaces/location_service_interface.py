from typing import Protocol

from app.models import Location


class LocationServiceInterface(Protocol):
    """Service for location-related operations."""

    def get_locations(self) -> list[Location]:
        """Return all known locations."""
        ...
