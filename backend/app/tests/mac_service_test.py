import sys
from pathlib import Path

from pytest import MonkeyPatch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.common.objects import AddressData
from app.database import Database
from app.database.models import Mac
from app.services import MacService


def make_address_data(mac: str = "aa:bb:cc:dd:ee:ff") -> AddressData:
    return AddressData(
        mac_address=mac,
        ip_address="192.0.2.1",
        ping_time_ms = 10,
        arp_time_ms = 5,
        hostname = "host",
        mac_vendor = "Vendor",
        os_guess = "Linux",
        ttl = 64,
    )


def test_save_mac_creates_new_mac():
    database = Database("sqlite:///:memory:")
    service = MacService(database)
    address_data = make_address_data()

    mac = service.save_mac(address_data, preserve=False)

    assert isinstance(mac, Mac)
    assert mac.address == address_data.mac_address
    assert mac.last_ip == address_data.ip_address
    assert mac.vendor == address_data.mac_vendor


def test_save_mac_preserve_fields():
    database = Database("sqlite:///:memory:")
    service = MacService(database)
    address_data = make_address_data()

    mac = service.save_mac(address_data, preserve=False)

    address_data_2 = make_address_data(mac.address)
    address_data_2.hostname = None
    address_data_2.mac_vendor = None
    address_data_2.os_guess = None
    address_data_2.ttl = None
    address_data_2.ping_time_ms = 20

    updated = service.save_mac(address_data_2, preserve=True)

    assert updated.hostname == mac.hostname
    assert updated.vendor == mac.vendor
    assert updated.ping_time_ms == 20


def test_get_by_address():
    database = Database("sqlite:///:memory:")
    service = MacService(database)

    address_data = make_address_data("00:00:00:00:00:01")
    mac = service.save_mac(address_data, preserve=False)

    found = service.get_mac_by_address(mac.address)
    assert found is not None
    assert found.address == mac.address


def test_get_vendor_from_mac(monkeypatch: MonkeyPatch) -> None:
    database = Database("sqlite:///:memory:")
    service = MacService(database)

    class FakeLookup:
        def lookup(self, mac: str) -> str:
            return "ACME Corp"

    monkeypatch.setattr("app.services.mac_service.MacLookup", lambda: FakeLookup())

    vendor = service.get_vendor_from_mac("aa:bb:cc:dd:ee:ff")
    assert vendor == "ACME Corp"
