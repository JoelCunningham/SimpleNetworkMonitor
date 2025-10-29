from app.database.interfaces import DatabaseInterface
from app.database.models import Device, Owner
from app.objects import OwnerInput
from app.services.interfaces import OwnerServiceInterface


class OwnerService(OwnerServiceInterface):
    """Service for handling owner-related operations."""

    def __init__(self, database: DatabaseInterface) -> None:
        self.database = database

    def get_owners(self) -> list[Owner]:
        """Get all owners."""
        return self.database.select_all(Owner).all()

    def add_owner(self, owner: OwnerInput) -> Owner:
        """Add a new owner to the database."""
        new_owner = Owner(
            name=owner.name,
            devices=self.database.select_all(Device).where_in(Device.id, owner.device_ids).all(),
        )

        self.database.create(new_owner)

        return new_owner

    def update_owner(self, id: int, owner: OwnerInput) -> Owner:
        """Update an existing owner."""
        existing_owner = self.database.select_by_id(Owner, id).first()
        if not existing_owner:
            raise ValueError("Owner not found")

        # replace with updated owner instance
        updated = Owner(
            id=id,
            name=owner.name,
            devices=self.database.select_all(Device).where_in(Device.id, owner.device_ids).all(),
        )

        # use create to upsert for simplicity (tests rely on returned object)
        self.database.create(updated)

        return updated

    def delete_owner(self, id: int) -> None:
        """Delete an owner from the database."""
        owner = self.database.select_by_id(Owner, id).first()
        if owner:
            self.database.delete(owner)
        else:
            raise ValueError("Owner not found")
        return None