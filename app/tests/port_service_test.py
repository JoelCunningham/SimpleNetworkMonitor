import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app import database
from app.models import Port
from app.objects import AddressData, PortInfo, ServiceInfo
from app.services import MacService, PortService


def test_save_port_persists():
    mac_svc = MacService(database)
    ad = AddressData(mac_address='aa:bb:cc:dd:ee:20', ip_address='192.0.2.20', ping_time_ms=1, arp_time_ms=1, hostname='h', mac_vendor='v', os_guess=None, ttl=64)
    m = mac_svc.save_mac(ad, preserve=False)

    port_svc = PortService(database)
    ports = [PortInfo(port=22, protocol='tcp', service='ssh')]
    services = {22: ServiceInfo(service_name='ssh', version=None)}

    port_svc.save_port(m, ports, services)

    found = database.select_all(Port).where(Port.mac_id == m.id).all()
    assert len(found) == 1
    assert found[0].port == 22
    assert found[0].service is not None and 'ssh' in found[0].service
