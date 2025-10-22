import sys
from pathlib import Path
from typing import Any, List, Optional, Type

import pytest
from sqlalchemy.orm.exc import DetachedInstanceError

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


from api.request.device_request import DeviceRequest
from app.models.mac import Mac
from app.objects.address_data import AddressData
from app.services.mac_service import MacService
from app.services.scanning_service import ScanningService


def device_to_dict(device: Any) -> dict[str, Any]:
    name = getattr(device, "name", None)
    model = getattr(device, "model", None)
    category_id = getattr(device, "category_id", None)

    try:
        macs: list[str | None] = []
        raw_macs = getattr(device, "macs", None)
        if raw_macs:
            for m in raw_macs:
                macs.append(getattr(m, "address", None))
    except DetachedInstanceError:
        # Try to fall back to primary_mac if available
        primary = getattr(device, "primary_mac", None)
        macs = [getattr(primary, "address", None)] if primary else []

    return {"name": name, "model": model, "category_id": category_id, "macs": [m for m in macs if m]}


# Minimal fake scan service used by ScanningService constructors in tests
class DummyScanService:
    def scan_network(self, scan_options: Any) -> list[AddressData]:
        return []


# Typed fake MacService used in tests
class FakeMacService(MacService):
    def get_mac_by_address(self, mac_address: str) -> Mac | None:
        # return a real Mac so relationships behave like production
        from datetime import datetime

        return Mac(address=mac_address, last_ip="0.0.0.0", last_seen=datetime.now())


# Typed fake ScanningService used in tests
class FakeScanningService(ScanningService):
    def __init__(self, scan_service: Any, results: Optional[list[AddressData]] = None) -> None:
        # initialize the real ScanningService with the provided stub
        super().__init__(scan_service=scan_service)  # type: ignore[arg-type]
        self._results = results or []

    def get_latest_results(self) -> list[AddressData]:
        return self._results


class DummyMac:
    def __init__(self, id: int | None = None, address: str = "") -> None:
        self.id = id
        self.address = address


class DummyDevice:
    def __init__(self, macs: Optional[List[DummyMac]] = None) -> None:
        self.macs = macs or []
        self.category_id = None
        self.name = None
        self.model = None
        self.location_id = None
        self.owner_id = None


class DummyDBQuery:
    def __init__(self, results: List[Any]) -> None:
        self._results = results

    def all(self) -> List[Any]:
        return self._results

    def first(self) -> Any | None:
        return self._results[0] if self._results else None

    def where_in(self, column: Any, values: List[int]) -> "DummyDBQuery":
        return DummyDBQuery([m for m in self._results if getattr(m, "id", None) in values])


class DummyDatabase:
    def __init__(self, devices: Optional[List[Any]] = None, macs: Optional[List[Any]] = None) -> None:
        self.devices: List[Any] = devices or []
        self.macs: List[Any] = macs or []

    def select_all(self, model: Type[Any]) -> DummyDBQuery:
        # return copies so callers can't accidentally mutate the DB's internal lists
        if getattr(model, "__name__", None) == "Device":
            return DummyDBQuery(list(self.devices))
        if getattr(model, "__name__", None) == "Mac":
            return DummyDBQuery(list(self.macs))
        return DummyDBQuery([])

    def select_by_id(self, model: Type[Any], id: int) -> DummyDBQuery:
        for d in self.devices:
            if getattr(d, "id", None) == id:
                return DummyDBQuery([d])
        return DummyDBQuery([])

    def create(self, instance: Any) -> None:
        # emulate SQLModel create: assign ID and append to devices
        instance.id = len(self.devices) + 1
        self.devices.append(instance)

    def update(self, instance: Any) -> None:
        # no-op for tests
        pass

    # helpers for tests
    def add_device(self, device: Any) -> None:
        device.id = len(self.devices) + 1
        self.devices.append(device)

    def add_mac(self, mac: Any) -> None:
        # accept either DummyMac or real Mac; if Mac, ensure required fields
        if isinstance(mac, Mac) and getattr(mac, "id", None) is None:
            mac.id = len(self.macs) + 1
        elif not hasattr(mac, "id") or getattr(mac, "id") is None:
            mac.id = len(self.macs) + 1
        self.macs.append(mac)


@pytest.fixture(autouse=True)
def patch_database(monkeypatch: pytest.MonkeyPatch) -> DummyDatabase:
    """Patch the app.database used by services to a dummy in-memory implementation."""
    import app
    import app.services.device_service as device_service_module
    import app.services.mac_service as mac_service_module
    import app.services.scanning_service as scanning_service_module

    dummy_db = DummyDatabase()
    monkeypatch.setattr(app, "database", dummy_db)
    # replace module-level database references
    monkeypatch.setattr(device_service_module, "database", dummy_db, raising=False)
    monkeypatch.setattr(mac_service_module, "database", dummy_db, raising=False)
    monkeypatch.setattr(scanning_service_module, "database", dummy_db, raising=False)
    return dummy_db


def make_device_request(
    name: str = "Device",
    model: str | None = None,
    category_id: int | None = None,
    location_id: int | None = None,
    owner_id: int | None = None,
    mac_ids: list[int] | None = None,
) -> DeviceRequest:
    """Small factory to create `DeviceRequest` instances for tests.

    Keeps tests concise and centralizes defaults.
    """
    return DeviceRequest(
        name=name,
        model=model or "",
        category_id=category_id or 0,
        location_id=location_id,
        owner_id=owner_id,
        mac_ids=mac_ids or [],
    )
