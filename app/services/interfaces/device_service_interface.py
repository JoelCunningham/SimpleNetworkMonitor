from typing import Protocol

from app.database.models import Device
from app.common.objects import DeviceInput


class DeviceServiceInterface(Protocol):
    """Interface for device related operations."""

    def get_devices(self) -> list[Device]:
        """Return a list of devices representing the current known devices."""
        ...

    def add_device(self, device: DeviceInput) -> Device:
        """Add a new device and return the created model."""
        ...

    def update_device(self, id: int, device: DeviceInput) -> Device:
        """Update an existing device by id and return the updated model."""
        ...
