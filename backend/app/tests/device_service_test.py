import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.common.objects import AddressData, DeviceInput
from app.database import Database
from app.services import DeviceService, MacService


def make_mac(database: Database, address: str = "aa:bb:cc:dd:ee:01") -> int:
    address_data = AddressData(
        mac_address=address,
        ip_address="192.0.2.1",
        ping_time_ms=1,
        arp_time_ms=1,
        hostname="h",
        mac_vendor="v",
        os_guess=None,
        ttl=64,
    )
    service = MacService(database)
    mac = service.save_mac(address_data, preserve=False)
    return mac.id


def test_add_device_creates_device():
    database = Database("sqlite:///:memory:")
    mac_id = make_mac(database)
    mac_service = MacService(database)

    device_service = DeviceService(database, mac_service)

    device_input = DeviceInput(name="TestDevice", model="ModelX", category_id=0, location_id=None, owner_id=None, mac_ids=[mac_id])
    device = device_service.add_device(device_input)

    assert device is not None
    assert device.name == "TestDevice"
    assert len(device.macs) == 1
    assert device.macs[0].id == mac_id


def test_update_device_updates_fields():
    database = Database("sqlite:///:memory:")
    mac_id = make_mac(database, "aa:bb:cc:dd:ee:02")
    mac_service = MacService(database)

    service = DeviceService(database, mac_service)

    device_input = DeviceInput(name="DeviceToUpdate", model="Old", category_id=0, location_id=None, owner_id=None, mac_ids=[mac_id])
    device = service.add_device(device_input)

    device_update = DeviceInput(name="DeviceToUpdate", model="NewModel", category_id=0, location_id=None, owner_id=None, mac_ids=[mac_id])
    updated_device = service.update_device(device.id, device_update)

    assert updated_device.model == "NewModel"
