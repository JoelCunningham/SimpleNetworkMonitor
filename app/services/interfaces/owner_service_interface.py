from typing import Protocol

from app.models import Owner
from common.objects import OwnerInput


class OwnerServiceInterface(Protocol):
    """Interface for owner-related operations."""

    def get_owners(self) -> list[Owner]:
        """Return all owners."""
        ...

    def add_owner(self, owner: OwnerInput) -> Owner:
        ...

    def update_owner(self, id: int, owner: OwnerInput) -> Owner:
        ...

    def delete_owner(self, id: int) -> None:
        ...
