import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.database import Database
from app.models import Discovery
from app.objects import AddressData, DiscoveryInfo
from app.services import DiscoveryService, MacService


def test_save_discoveries_persists():
    database = Database("sqlite:///:memory:")
    mac_service = MacService(database)
    address_data = AddressData(mac_address="aa:bb:cc:dd:ee:10", ip_address="192.0.2.10", ping_time_ms=1, arp_time_ms=1, hostname="h", mac_vendor="v", os_guess=None, ttl=64)
    mac = mac_service.save_mac(address_data, preserve=False)

    service = DiscoveryService(database)
    infos = [DiscoveryInfo(protocol="mdns", device_name="DeviceA", device_type="mDNS/Bonjour Device")]
    service.save_discoveries(mac, infos)

    found = database.select_all(Discovery).where(Discovery.mac_id == mac.id).all()
    assert len(found) == 1
    assert found[0].device_name == "DeviceA"
