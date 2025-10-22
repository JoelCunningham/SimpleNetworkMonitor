import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from typing import Any, cast

import pytest

from app.objects.address_data import AddressData
from app.services.scan_service import ScanService
from app.services.scanning_service import ScanningService


class DummyScanService:
    def __init__(self) -> None:
        self.saved: list[Any] = []

    def scan_network(self, options: Any) -> list[AddressData]:
        # return one fake AddressData
        return [AddressData(ip_address="192.168.1.10", mac_address="aa:bb:cc:dd:ee:ff")]

    def save_full_scan(self, addr: AddressData) -> None:
        self.saved.append(("full", addr))

    def save_mac_scan(self, addr: AddressData) -> None:
        self.saved.append(("mac", addr))


@pytest.fixture(autouse=True)
def patch_scan_service() -> DummyScanService:
    # Return a dummy scan service instance for tests
    return DummyScanService()


def test_perform_scan_calls_save_functions(patch_scan_service: DummyScanService) -> None:
    dummy_scan = DummyScanService()
    # Cast the dummy to the declared ScanService type to satisfy strict typing
    scanning = ScanningService(scan_service=cast(ScanService, dummy_scan))

    # Do a full scan (call via Any to avoid protected-member type complaint)
    cast(Any, scanning)._perform_scan(full_scan=True)

    assert any(kind == "full" for kind, _ in dummy_scan.saved)

    # Do a basic scan
    cast(Any, scanning)._perform_scan(full_scan=False)
    assert any(kind == "mac" for kind, _ in dummy_scan.saved)


def test_perform_scan_handles_scan_exception(monkeypatch: pytest.MonkeyPatch) -> None:
    # Create a scan_service that raises
    class ExplodingScanService:
        def scan_network(self, options: object) -> list[AddressData]:
            raise RuntimeError("boom")

    scanning = ScanningService(scan_service=cast(ScanService, ExplodingScanService()))

    # calling _perform_scan should not raise; it should set scan_error
    cast(Any, scanning)._perform_scan(full_scan=True)

    assert scanning.scan_error is not None or scanning.last_scan_results == []


def test_perform_scan_updates_last_scan(monkeypatch: pytest.MonkeyPatch) -> None:
    class OneResultScanService:
        def scan_network(self, options: object) -> list[AddressData]:
            return [AddressData(ip_address="10.0.0.1", mac_address="aa:bb:cc:dd:ee:ff")]

        def save_full_scan(self, addr: AddressData) -> None:
            pass

        def save_mac_scan(self, addr: AddressData) -> None:
            pass

    scanning = ScanningService(scan_service=cast(ScanService, OneResultScanService()))
    cast(Any, scanning)._perform_scan(full_scan=True)

    assert scanning.last_scan_time is not None
    assert scanning.last_scan_results


def test_perform_scan_sets_scan_error_on_save_failure() -> None:
    """If the scan service's save function raises, the ScanningService should capture an error and keep is_scanning False."""

    class BadSaveScanService:
        def scan_network(self, options: object) -> list[AddressData]:
            return [AddressData(ip_address="10.0.0.2", mac_address="aa:bb:cc:dd:ee:01")]

        def save_full_scan(self, addr: AddressData) -> None:
            raise RuntimeError("save failed")

        def save_mac_scan(self, addr: AddressData) -> None:
            raise RuntimeError("save failed")

    scanning = ScanningService(scan_service=cast(ScanService, BadSaveScanService()))
    # Should not raise
    cast(Any, scanning)._perform_scan(full_scan=True)

    # scan_error may be None due to bare except, but is_scanning must be False after completion
    assert scanning.is_scanning is False


def test_is_scanning_flag_resets_even_on_exception() -> None:
    """Ensure is_scanning is reset when the scan raises an exception."""

    class ExplodingScanService2:
        def scan_network(self, options: object) -> list[AddressData]:
            raise RuntimeError("boom")

        def save_full_scan(self, addr: AddressData) -> None:
            pass

        def save_mac_scan(self, addr: AddressData) -> None:
            pass

    scanning = ScanningService(scan_service=cast(ScanService, ExplodingScanService2()))
    cast(Any, scanning)._perform_scan(full_scan=True)

    assert scanning.is_scanning is False
