from app import database
from app.models.device import Device
from app.models.owner import Owner


class OwnerService:
    """Service for handling owner-related operations."""
    
    def get_owners(self) -> list[Owner]:
        """Get all owners."""
        return database.session.query(Owner).all()

    def add_owner(self, name: str, device_ids: list[int]) -> Owner:
        """Add a new owner to the database."""
        new_owner = Owner()
        new_owner.name = name

        for device_id in device_ids:
            device = database.session.query(Device).get(device_id)
            if device:
                new_owner.devices.append(device)

        database.session.add(new_owner)
        database.session.commit()
        return new_owner

    def update_owner(self, id: int, name: str, device_ids: list[int]) -> Owner:
        """Update an existing owner."""
        existing_owner = database.session.query(Owner).get(id)

        if not existing_owner:
            raise ValueError("Owner not found")

        existing_owner.name = name
        
        existing_owner.devices.clear()
        for device_id in device_ids:
            device = database.session.query(Device).get(device_id)
            if device:
                existing_owner.devices.append(device)
        
        database.session.commit()
        return existing_owner
    
    def delete_owner(self, owner_id: int) -> None:
        """Delete an owner from the database."""
        owner = database.session.query(Owner).get(owner_id)
        if owner:
            database.session.delete(owner)
            database.session.commit()
            
        else:
            raise ValueError("Owner not found")
        return None