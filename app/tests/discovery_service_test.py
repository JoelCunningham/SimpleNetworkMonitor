import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app import database
from app.models import Discovery
from app.objects import AddressData, DiscoveryInfo
from app.services import DiscoveryService, MacService


def test_save_discoveries_persists():
    mac_svc = MacService(database)
    ad = AddressData(mac_address="aa:bb:cc:dd:ee:10", ip_address="192.0.2.10", ping_time_ms=1, arp_time_ms=1, hostname="h", mac_vendor="v", os_guess=None, ttl=64)
    mac = mac_svc.save_mac(ad, preserve=False)

    svc = DiscoveryService(database)
    infos = [DiscoveryInfo(protocol="mdns", device_name="DeviceA", device_type="mDNS/Bonjour Device")]
    svc.save_discoveries(mac, infos)

    found = database.select_all(Discovery).where(Discovery.mac_id == mac.id).all()
    assert len(found) == 1
    assert found[0].device_name == "DeviceA"
