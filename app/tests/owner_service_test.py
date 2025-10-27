import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.database import Database
from app.objects import OwnerInput
from app.services import OwnerService


def test_get_owners_empty():
    database = Database("sqlite:///:memory:")
    svc = OwnerService(database)

    owners = svc.get_owners()
    assert isinstance(owners, list)
    assert len(owners) == 0


def test_add_owner_and_get():
    database = Database("sqlite:///:memory:")
    svc = OwnerService(database)

    oi = OwnerInput(name="Alice", device_ids=[])
    svc.add_owner(oi)

    owners = svc.get_owners()
    assert len(owners) == 1
    assert owners[0].name == "Alice"
