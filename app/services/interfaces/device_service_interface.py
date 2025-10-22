from typing import Protocol, Any


class DeviceServiceInterface(Protocol):
    """Interface for device-related operations."""

    def get_all_devices(self) -> list[Any]:
        ...

    def get_device(self, id: int) -> Any | None:
        ...

    def save_device(self, device: Any) -> Any:
        ...

    def delete_device(self, id: int) -> None:
        ...
