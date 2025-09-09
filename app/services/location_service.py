from app import database
from app.models.location import Location


class LocationService:
    """Service for handling location-related operations."""

    def get_locations(self) -> list[Location]:
        """Get all device locations."""
        return database.select_all(Location).all()
    
    