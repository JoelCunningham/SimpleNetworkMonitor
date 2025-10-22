from app.database import Database
from app.models import Location
from app.services.interfaces import LocationServiceInterface


class LocationService(LocationServiceInterface):
    """Service for handling location-related operations."""

    def __init__(self, database: Database) -> None:
        self.database = database

    def get_locations(self) -> list[Location]:
        return self.database.select_all(Location).all()
