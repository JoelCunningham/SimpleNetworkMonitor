from app import database
from app.models.device import Device
from app.models.owner import Owner
from common.objects.owner_input import OwnerInput


class OwnerService:
    """Service for handling owner-related operations."""
    
    def get_owners(self) -> list[Owner]:
        """Get all owners."""
        return database.select_all(Owner).all()

    def add_owner(self, owner: OwnerInput) -> Owner:
        """Add a new owner to the database."""
        new_owner = Owner(
            name=owner.name,
            devices=database.select_all(Device).where_in(Device.id, owner.device_ids).all()
        )
    
        database.save(new_owner)
        
        return new_owner

    def update_owner(self, id: int, owner: OwnerInput) -> Owner:
        """Update an existing owner."""
        existing_owner = database.select_all(Owner).where(Owner.id == id).first()
        if not existing_owner:
            raise ValueError("Owner not found")

        existing_owner = Owner(
            id=id,
            name=owner.name,
            devices=database.select_all(Device).where_in(Device.id, owner.device_ids).all()
        )
        
        database.save(existing_owner)

        return existing_owner
    
    def delete_owner(self, owner_id: int) -> None:
        """Delete an owner from the database."""
        owner = database.select_by_id(Owner, owner_id).first()
        if owner:
            database.delete(owner)
        else:
            raise ValueError("Owner not found")
        return None