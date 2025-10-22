import sys
from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from typing import List

from app.objects import PortInfo, DiscoveryInfo, ServiceInfo

from app.database import Database
from app.services.mac_service import MacService
from app.services.scan_service import ScanService
from app.objects.address_data import AddressData
from app.models.mac import Mac


def test_get_latest_scan_date():
    database = Database("sqlite:///:memory:")
    mac_svc = MacService(database)
    address_data = AddressData(
        mac_address="aa:bb:cc:dd:ee:99",
        ip_address="192.0.2.99",
        ping_time_ms=1,
        arp_time_ms=1,
        hostname=None,
        mac_vendor=None,
        os_guess=None,
        ttl=64,
    )
    mac_svc.save_mac(address_data, preserve=False)

    class FakePing:
        def ping(self, ip_address: str) -> tuple[bool | None, int, str | None]:
            # success, rtt_ms, stdout (or None)
            return True, 1, ""

        def get_ttl_from_ping(self, ping_result: str) -> int | None:
            return None

        def get_hostname(self, ip_address: str) -> str | None:
            return None

        def get_os_from_ttl(self, ttl: int) -> str:
            return ""

    class FakePort:
        def scan_ports(self, ip_address: str, ports: List[int]) -> list[PortInfo]:
            return []

        def save_port(self, mac_record: Mac, open_ports: list[PortInfo], services_info: dict[int, ServiceInfo] | None) -> None:
            # noop persistence for tests
            return None

    class FakeDiscovery:
        def discover_netbios(self, ip_address: str) -> DiscoveryInfo | None:
            return None

        def discover_upnp(self, ip_address: str) -> DiscoveryInfo | None:
            return None

        def discover_mdns(self, ip_address: str) -> DiscoveryInfo | None:
            return None

        def save_discoveries(self, mac: Mac, discoveries: list[DiscoveryInfo]) -> None:
            # noop persistence for tests
            return None

    class FakeProtocol:
        # Use parameter names that match the Protocol interface for compatibility
        def detect_http(self, ip: str, port: int) -> ServiceInfo | None:
            return None

        def detect_ssh(self, ip: str, port: int) -> ServiceInfo | None:
            return None

        def detect_banner(self, ip: str, port: int, service_name: str) -> ServiceInfo | None:
            return None

    service = ScanService(database, FakePing(), mac_svc, FakePort(), FakeDiscovery(), FakeProtocol())

    latest = service.get_latest_scan_date()
    assert isinstance(latest, datetime)