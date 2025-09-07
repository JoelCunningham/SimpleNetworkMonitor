from app import database
from app.models.device import Device
from app.models.mac import Mac
from app.services.mac_service import MacService
from app.services.scanning_service import ScanningService


class DeviceService:
    """Service for handling device-related operations."""

    def __init__(self, mac_service: MacService, scanning_service: ScanningService) -> None:
        self.mac_service = mac_service
        self.scanning_service = scanning_service

    def get_current_devices(self,) -> list[Device]:
        """Get all devices from database."""
        
        devices = database.session.query(Device).all()
        scanned_devices = self.scanning_service.get_latest_results()
            
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

    def add_device(self, name: str, model:str, category_id: int, location_id: int, owner_id: int, mac_ids: list[int]) -> Device:
        """Save a device to the database."""
        new_device = Device()
        
        new_device.name = name
        new_device.model = model
        new_device.category_id = category_id
        new_device.location_id = location_id
        new_device.owner_id = owner_id
        
        existing_macs = database.session.query(Mac).filter(Mac.id.in_(mac_ids)).all()
        new_device.macs.extend(existing_macs)
        
        database.session.add(new_device)
        database.session.commit()
        
        return new_device
    
    def update_device(self, id: int, name: str, model:str, category_id: int, location_id: int, owner_id: int, mac_ids: list[int]) -> Device:
        """Update an existing device."""
        existing_device = database.session.get(Device, id)
        
        if not existing_device:
            raise ValueError("Device not found")
        
        if not mac_ids:
            raise ValueError("At least one MAC address is required")
        
        existing_device.name = name
        existing_device.model = model
        existing_device.category_id = category_id
        existing_device.location_id = location_id
        existing_device.owner_id = owner_id
        
        existing_device.macs.all().clear()
        for mac_id in mac_ids:
            mac = database.session.get(Mac, mac_id)
            if mac:
                existing_device.macs.append(mac)
            else:
                raise ValueError(f"MAC with ID {mac_id} not found")
        
        database.session.commit()
        
        return existing_device

    def get_device(self, mac_address: str) -> Device | None:
        """Get a device by its MAC address."""
        return database.session.query(Device).join(Mac).filter(Mac.address == mac_address).first()
    