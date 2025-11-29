import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from app.services import PingService


def test_get_ttl_from_ping():
    ping_out = "64 bytes from 192.168.0.1: icmp_seq=1 ttl=64 time=0.123 ms"
    service = PingService()
    ttl = service.get_ttl_from_ping(ping_out)
    assert ttl == 64


def test_get_os_from_ttl_exact():
    service = PingService()
    assert service.get_os_from_ttl(64) == "Linux/Unix/macOS"
    assert service.get_os_from_ttl(128).startswith("Windows")


def test_get_os_from_ttl_via_router():
    service = PingService()
    # TTL of 62 (within 60 +/-10) should map via router to Other Linux
    assert "via router" in service.get_os_from_ttl(62)
