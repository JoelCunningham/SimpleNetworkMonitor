from typing import Protocol, Any


class MacServiceInterface(Protocol):
    """Interface for MAC/ARP resolution and storage."""

    def resolve_mac_address(self, ip_address: str) -> tuple[str, int] | None:
        ...

    def save_mac(self, address_data: Any, mac_only: bool) -> Any:
        ...

    def get_vendor_from_mac(self, mac: str) -> str | None:
        ...

    def get_all_macs(self) -> list[Any]:
        ...
