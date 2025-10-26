from typing import Protocol

from app.models import Device
from app.objects import DeviceInput


class DeviceServiceInterface(Protocol):
    """Interface for device related operations."""

    def get_current_devices(self) -> list[Device]:
        """Return a list of devices representing the current known devices."""
        ...

    def add_device(self, device: DeviceInput) -> Device:
        """Add a new device and return the created model."""
        ...

    def update_device(self, id: int, device: DeviceInput) -> Device:
        """Update an existing device by id and return the updated model."""
        ...
