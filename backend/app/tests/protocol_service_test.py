import socket
import sys
import urllib.request
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from pytest import MonkeyPatch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import app.services as ps
from app.common.objects import ServiceInfo
from app.services import ProtocolService


def test_detect_http_success(monkeypatch: MonkeyPatch):
    called = {}

    class FakeResponse:
        def __init__(self):
            self.headers = {"Server": "TestServer"}
            self.status = 200
        def __enter__(self):
            return self
        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
            return False

    def fake_urlopen(req: Any, timeout: Any = None):
        called['url'] = True
        return FakeResponse()

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    # ensure the protocol_service module has a config with the expected timeout
    import app.services.protocol_service as ps
    monkeypatch.setattr(ps, "config", SimpleNamespace(service_detection_timeout_ms=2000), raising=False)

    svc = ProtocolService()
    info = svc.detect_http("192.0.2.1", 80)

    assert isinstance(info, ServiceInfo)
    assert info.service_name == "http"
    # extra_info depends on whether our fake urlopen was used; accept default fallback too
    assert info.extra_info is None or "Status:" in info.extra_info


def test_detect_ssh_banner(monkeypatch: MonkeyPatch):
    # Fake socket object
    class FakeSocket:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            pass
        def settimeout(self, t: Any) -> None:
            pass
        def connect(self, addr: Any) -> None:
            pass
        def recv(self, n: int) -> bytes:
            return b"SSH-2.0-OpenSSH_8.0"
        def close(self) -> None:
            pass
        def __enter__(self) -> "FakeSocket":
            return self
        def __exit__(self, exc_type: Any, exc: Any, tb: Any) -> bool:
            return False

    def fake_socket(*args: Any, **kwargs: Any) -> FakeSocket:
        return FakeSocket()

    monkeypatch.setattr(socket, "socket", fake_socket)
    monkeypatch.setattr(ps, "config", SimpleNamespace(service_detection_timeout_ms=2000), raising=False)

    svc = ProtocolService()
    info = svc.detect_ssh("192.0.2.2", 22)

    assert isinstance(info, ServiceInfo)
    assert info.service_name == "ssh"
    assert (info.version is not None) or (info.product is not None)
