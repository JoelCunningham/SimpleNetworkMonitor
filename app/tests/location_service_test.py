import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.database import Database
from app.models import Location
from app.services import LocationService


def test_get_locations_empty():
    database = Database("sqlite:///:memory:")
    service = LocationService(database)

    locations = service.get_locations()
    assert isinstance(locations, list)
    assert len(locations) == 0


def test_get_locations_after_create():
    database = Database("sqlite:///:memory:")
    service = LocationService(database)

    location = Location(name="Lab")
    database.create(location)

    locations = service.get_locations()
    assert len(locations) == 1
    assert locations[0].name == "Lab"
