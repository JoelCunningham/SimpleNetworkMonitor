import sys
from pathlib import Path

import pytest

from app.tests.conftest import (DummyDatabase, DummyDevice, DummyMac,
                                DummyScanService, FakeMacService,
                                FakeScanningService, device_to_dict)

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.models.mac import Mac
from app.objects.address_data import AddressData
from app.services.device_service import DeviceService
from app.tests.conftest import make_device_request
from common.objects.device_input import DeviceInput


def test_get_current_devices_merges_scanned_without_db_device(
    patch_database: DummyDatabase
) -> None:
    """When the scanner finds a MAC that isn't in the DB, a new Device wrapper is returned."""
    # Setup DB has one device with a mac
    db = patch_database
    db.add_device(DummyDevice(macs=[DummyMac(1, "aa:bb:cc:dd:ee:ff")]))

    # Scanning service returns a device with a different mac not in DB
    scanned = [AddressData(ip_address="192.168.1.5", mac_address="11:22:33:44:55:66")]

    mac_service = FakeMacService()
    scanning_service_inst = FakeScanningService(DummyScanService(), results=scanned)

    device_service = DeviceService(mac_service=mac_service, scanning_service=scanning_service_inst)

    devices = device_service.get_current_devices()

    # Expect that the scanned mac was wrapped into a Device and appended
    all_macs: set[str] = set()
    for d in devices:
        dto = device_to_dict(d)
        all_macs.update(dto["macs"])  
    assert "11:22:33:44:55:66" in all_macs


def test_add_device_creates_device_with_macs(patch_database: DummyDatabase) -> None:
    """Adding a device persists it to the database and attaches existing Mac records."""
    db = patch_database
    # Pre-seed macs in DB
    from datetime import datetime
    db.add_mac(Mac(address="aa:aa:aa:aa:aa:aa", last_ip="0.0.0.0", last_seen=datetime.now()))
    db.add_mac(Mac(address="bb:bb:bb:bb:bb:bb", last_ip="0.0.0.0", last_seen=datetime.now()))

    # Use noop fakes from conftest when available
    ds = DeviceService(mac_service=FakeMacService(), scanning_service=FakeScanningService(DummyScanService(), results=[]))

    # Use the Pydantic request model to simulate API input and convert to DeviceInput as the route does
    # Use the ids assigned by DummyDatabase.add_mac()
    mac_ids = [db.macs[0].id, db.macs[1].id]
    device_request = make_device_request(name="Router", model="XR100", category_id=1, location_id=None, owner_id=None, mac_ids=mac_ids)
    dto = DeviceInput(**device_request.model_dump())

    new_device = ds.add_device(dto)

    assert new_device is not None
    dto = device_to_dict(new_device)
    assert dto["name"] == "Router"
    assert set(dto["macs"]) == {db.macs[0].address, db.macs[1].address}
    # ensure the dummy database recorded the new device (persistence check)
    assert any(getattr(d, "name", None) == "Router" for d in db.devices)


def test_update_device_raises_when_not_found(patch_database: DummyDatabase) -> None:
    """Updating a non-existent device should raise a ValueError."""
    # use typed fakes instead of SimpleNamespace doubles
    mac_service = FakeMacService()
    scanning_service = FakeScanningService(DummyScanService(), results=[])
    ds = DeviceService(mac_service=mac_service, scanning_service=scanning_service)

    # Use DeviceRequest (pydantic) to produce the DTO used by the service layer
    device_request = make_device_request(name="X", model="Y", category_id=1, location_id=None, owner_id=None, mac_ids=[1])
    dto = DeviceInput(**device_request.model_dump())

    with pytest.raises(ValueError):
        ds.update_device(999, dto)


def test_update_device_success_updates_fields_and_macs(patch_database: DummyDatabase) -> None:
    """Updating an existing device should modify its fields and associated Macs."""
    db = patch_database
    from datetime import datetime

    # create two macs and a device that currently has mac1
    mac1 = Mac(address="00:11:22:33:44:55", last_ip="0.0.0.0", last_seen=datetime.now())
    mac2 = Mac(address="66:77:88:99:AA:BB", last_ip="0.0.0.0", last_seen=datetime.now())
    db.add_mac(mac1)
    db.add_mac(mac2)

    # Create a minimal device object that can hold Mac instances
    class TestDevice:
        def __init__(self, macs: list[Mac]) -> None:
            self.macs = macs
            self.id: int | None = None

    device = TestDevice(macs=[mac1])
    db.add_device(device)

    ds = DeviceService(mac_service=FakeMacService(), scanning_service=FakeScanningService(DummyScanService(), results=[]))

    # Update to use mac2 and new name
    device_request = make_device_request(name="Updated", model="M2", category_id=3, location_id=None, owner_id=None, mac_ids=[mac2.id])
    dto = DeviceInput(**device_request.model_dump())

    assert device.id is not None
    updated = ds.update_device(device.id, dto)

    updated_d = device_to_dict(updated)
    assert updated_d["name"] == "Updated"
    assert set(updated_d["macs"]) == {mac2.address}
    # ensure database entry was updated as well
    assert any(getattr(d, "name", None) == "Updated" for d in db.devices)


def test_add_device_with_invalid_mac_ids_creates_device_with_no_macs(patch_database: DummyDatabase) -> None:
    """Adding a device with non-existing mac IDs should create the device but attach no Macs."""
    # db fixture used above
    ds = DeviceService(mac_service=FakeMacService(), scanning_service=FakeScanningService(DummyScanService(), results=[]))

    device_request = make_device_request(name="NoMacs", model="M0", category_id=1, location_id=None, owner_id=None, mac_ids=[999])
    dto = DeviceInput(**device_request.model_dump())

    new_device = ds.add_device(dto)
    d = device_to_dict(new_device)
    assert d["name"] == "NoMacs"
    assert d["macs"] == []
    # verify persistence
    assert any(getattr(x, "name", None) == "NoMacs" for x in patch_database.devices)


def test_get_current_devices_does_not_modify_db_when_scanner_adds_temp_device(patch_database: DummyDatabase) -> None:
    """get_current_devices should not persist scanner-only devices into the DB."""
    db = patch_database
    # seed a single device
    db.add_device(DummyDevice(macs=[DummyMac(1, "aa:bb:cc:dd:ee:ff")]))
    before_count = len(db.devices)

    scanned = [AddressData(ip_address="192.168.1.5", mac_address="11:22:33:44:55:66")]
    ds = DeviceService(mac_service=FakeMacService(), scanning_service=FakeScanningService(DummyScanService(), results=scanned))

    _ = ds.get_current_devices()

    assert len(db.devices) == before_count


def test_get_current_devices_ignores_scanned_when_mac_service_returns_none(patch_database: DummyDatabase) -> None:
    """If MacService can't resolve an address, scanned entries should not be added to view."""
    db = patch_database
    db.add_device(DummyDevice(macs=[DummyMac(1, "aa:bb:cc:dd:ee:ff")]))

    # scanning returns a mac not in DB
    scanned = [AddressData(ip_address="192.168.1.5", mac_address="11:22:33:44:55:66")]

    class NoneMacService(FakeMacService):
        def get_mac_by_address(self, mac_address: str):
            return None

    ds = DeviceService(mac_service=NoneMacService(), scanning_service=FakeScanningService(DummyScanService(), results=scanned))

    devices = ds.get_current_devices()
    all_macs = {m for d in devices for m in device_to_dict(d)["macs"]}

    assert "11:22:33:44:55:66" not in all_macs


def test_update_device_requires_at_least_one_mac(patch_database: DummyDatabase) -> None:
    """update_device should raise when mac_ids is empty."""
    db = patch_database

    # create a device to update
    class TestDevice:
        def __init__(self) -> None:
            self.macs = []
            self.id: int | None = None

    dev = TestDevice()
    db.add_device(dev)

    ds = DeviceService(mac_service=FakeMacService(), scanning_service=FakeScanningService(DummyScanService(), results=[]))

    device_request = make_device_request(name="NoMacUpdate", model="M", category_id=1, mac_ids=[])
    dto = DeviceInput(**device_request.model_dump())

    assert dev.id is not None
    with pytest.raises(ValueError):
        ds.update_device(dev.id, dto)


def test_add_device_assigns_id_and_persists(patch_database: DummyDatabase) -> None:
    """add_device should assign an id and persist the device in the DummyDatabase."""
    db = patch_database
    from datetime import datetime

    db.add_mac(Mac(address="aa:aa:aa:aa:aa:aa", last_ip="0.0.0.0", last_seen=datetime.now()))

    ds = DeviceService(mac_service=FakeMacService(), scanning_service=FakeScanningService(DummyScanService(), results=[]))
    device_request = make_device_request(name="PersistMe", model="M1", category_id=2, mac_ids=[db.macs[0].id])
    dto = DeviceInput(**device_request.model_dump())

    new_device = ds.add_device(dto)

    assert getattr(new_device, "id", None) is not None
    assert any(getattr(d, "id", None) == new_device.id for d in db.devices)
