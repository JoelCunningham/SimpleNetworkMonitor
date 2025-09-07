from app import database
from app.models.category import Category
from app.models.device import Device
from app.models.location import Location
from app.models.mac import Mac
from app.models.owner import Owner
from app.objects.address_data import AddressData
from app.services.mac_service import MacService


class DeviceService:
    """Service for handling device-related operations."""
    
    def __init__(self, mac_service: MacService) -> None:
        self.mac_service = mac_service
        
    def get_current_devices(self, scanned_devices: list[AddressData]) -> list[Device]:
        """Get all devices from database."""
        
        devices = database.session.query(Device).all()
            
        for device_data in scanned_devices:
            if device_data.mac_address:
                has_device = any(device_data.mac_address == mac.address for device in devices for mac in device.macs.all())
                if not has_device:
                    mac_data = self.mac_service.get_mac_by_address(device_data.mac_address)                
                    if mac_data: 
                        device = Device()
                        device.macs.append(mac_data)
                        device.category_id = 0
                        devices.append(device)
        
        return devices

    def add_device(self, model:str, category_id: int, location_id: int, owner_id: int, mac_ids: list[int]) -> Device:
        """Save a device to the database."""
        new_device = Device()
        
        new_device.model = model
        new_device.category_id = category_id
        new_device.location_id = location_id
        new_device.owner_id = owner_id
        
        existing_macs = database.session.query(Mac).filter(Mac.id.in_(mac_ids)).all()
        new_device.macs.extend(existing_macs)
        
        database.session.add(new_device)
        database.session.commit()
        
        return new_device

    def get_device(self, mac_address: str) -> Device | None:
        """Get a device by its MAC address."""
        return database.session.query(Device).join(Mac).filter(Mac.address == mac_address).first()

    def get_device_locations(self) -> list[Location]:
        """Get all device locations."""
        return database.session.query(Location).all()
    
    def get_device_categories(self) -> list[Category]:
        """Get all device categories."""
        return database.session.query(Category).all()
    
    def get_device_owners(self) -> list[Owner]:
        """Get all device owners."""
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