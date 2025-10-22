import sys
from pathlib import Path

from pytest import MonkeyPatch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app import database
from app.models import Mac
from app.objects import AddressData
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
    svc = MacService(database)
    ad = make_address_data()

    mac = svc.save_mac(ad, preserve=False)

    assert isinstance(mac, Mac)
    assert mac.address == ad.mac_address
    assert mac.last_ip == ad.ip_address
    assert mac.vendor == ad.mac_vendor


def test_save_mac_preserve_fields():
    svc = MacService(database)
    ad = make_address_data()

    mac = svc.save_mac(ad, preserve=False)

    ad2 = make_address_data(mac.address)
    ad2.hostname = None
    ad2.mac_vendor = None
    ad2.os_guess = None
    ad2.ttl = None
    ad2.ping_time_ms = 20

    updated = svc.save_mac(ad2, preserve=True)

    assert updated.hostname == mac.hostname
    assert updated.vendor == mac.vendor
    assert updated.ping_time_ms == 20


def test_get_by_address():
    svc = MacService(database)

    ad = make_address_data("00:00:00:00:00:01")
    mac = svc.save_mac(ad, preserve=False)

    found = svc.get_mac_by_address(mac.address)
    assert found is not None
    assert found.address == mac.address


def test_get_vendor_from_mac(monkeypatch: MonkeyPatch) -> None:
    svc = MacService(database)

    class FakeLookup:
        def lookup(self, mac: str) -> str:
            return "ACME Corp"

    monkeypatch.setattr("app.services.mac_service.MacLookup", lambda: FakeLookup())

    vendor = svc.get_vendor_from_mac("aa:bb:cc:dd:ee:ff")
    assert vendor == "ACME Corp"
