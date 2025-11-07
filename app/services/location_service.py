from app.database.interfaces import DatabaseInterface
from app.database.models import Location
from app.services.interfaces import LocationServiceInterface


class LocationService(LocationServiceInterface):
    """Service for handling location-related operations."""

    def __init__(self, database: DatabaseInterface) -> None:
        self.database = database

    def get_locations(self) -> list[Location]:
        return self.database.select(Location).all()
