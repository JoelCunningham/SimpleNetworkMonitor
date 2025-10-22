import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app import database
from app.objects import AddressData
from app.services import DeviceService, MacService
from common.objects import DeviceInput


def make_mac(address: str = "aa:bb:cc:dd:ee:01") -> int:
    ad = AddressData(
        mac_address=address,
        ip_address="192.0.2.1",
        ping_time_ms=1,
        arp_time_ms=1,
        hostname="h",
        mac_vendor="v",
        os_guess=None,
        ttl=64,
    )
    svc = MacService(database)
    mac = svc.save_mac(ad, preserve=False)
    return mac.id


def test_add_device_creates_device():
    mac_id = make_mac()
    mac_svc = MacService(database)
    class FakeScanner:
        def get_latest_results(self) -> list[AddressData]:
            return []

    svc = DeviceService(database, mac_svc, FakeScanner())

    di = DeviceInput(name="TestDevice", model="ModelX", category_id=0, location_id=None, owner_id=None, mac_ids=[mac_id])
    dev = svc.add_device(di)

    assert dev is not None
    assert dev.name == "TestDevice"
    assert len(dev.macs) == 1
    assert dev.macs[0].id == mac_id


def test_update_device_updates_fields():
    mac_id = make_mac("aa:bb:cc:dd:ee:02")
    mac_svc = MacService(database)
    class FakeScanner:
        def get_latest_results(self) -> list[AddressData]:
            return []

    svc = DeviceService(database, mac_svc, FakeScanner())

    di = DeviceInput(name="DeviceToUpdate", model="Old", category_id=0, location_id=None, owner_id=None, mac_ids=[mac_id])
    dev = svc.add_device(di)

    upd = DeviceInput(name="DeviceToUpdate", model="NewModel", category_id=0, location_id=None, owner_id=None, mac_ids=[mac_id])
    updated = svc.update_device(dev.id, upd)

    assert updated.model == "NewModel"
