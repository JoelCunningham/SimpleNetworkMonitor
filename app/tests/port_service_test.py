import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.database import Database
from app.database.models import Port
from app.common.objects import AddressData, PortInfo, ServiceInfo
from app.services import MacService, PortService


def test_save_port_persists():
    database = Database("sqlite:///:memory:")
    mac_service = MacService(database)
    address_data = AddressData(mac_address='aa:bb:cc:dd:ee:20', ip_address='192.0.2.20', ping_time_ms=1, arp_time_ms=1, hostname='h', mac_vendor='v', os_guess=None, ttl=64)
    mac = mac_service.save_mac(address_data, preserve=False)

    port_service = PortService(database)
    ports = [PortInfo(number=22, protocol='tcp', service='ssh')]
    services = {22: ServiceInfo(service_name='ssh', version=None)}

    port_service.save_port(mac, ports, services)

    found = database.select(Port).where(Port.mac_id == mac.id).all()
    assert len(found) == 1
    assert found[0].number == 22
    assert found[0].service is not None and 'ssh' in found[0].service
