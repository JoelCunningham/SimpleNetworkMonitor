import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app import database
from app.models import Location
from app.services import LocationService


def test_get_locations_empty():
    svc = LocationService(database)

    locs = svc.get_locations()
    assert isinstance(locs, list)
    assert len(locs) == 0


def test_get_locations_after_create():
    svc = LocationService(database)

    loc = Location(name="Lab")
    database.create(loc)

    locs = svc.get_locations()
    assert len(locs) == 1
    assert locs[0].name == "Lab"
