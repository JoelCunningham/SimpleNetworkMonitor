from app import database
from app.models.device import Device
from app.models.mac import Mac
from app.services.mac_service import MacService
from app.services.scanning_service import ScanningService
from common.objects.device_input import DeviceInput


class DeviceService:
    """Service for handling device-related operations."""

    def __init__(self, mac_service: MacService, scanning_service: ScanningService) -> None:
        self.mac_service = mac_service
        self.scanning_service = scanning_service

    def get_current_devices(self,) -> list[Device]:
        """Get all devices from database."""    
        devices = database.select_all(Device).all()
        scanned_devices = self.scanning_service.get_latest_results()
            
        for device_data in scanned_devices:
            if device_data.mac_address:
                has_device = any(device_data.mac_address == mac.address for device in devices for mac in device.macs)
                if not has_device:
                    mac_data = self.mac_service.get_mac_by_address(device_data.mac_address)                
                    if mac_data: 
                        device = Device()
                        device.macs.append(mac_data)
                        device.category_id = 0
                        devices.append(device)
        
        return devices

    def add_device(self, device: DeviceInput) -> Device:
        """Save a device to the database."""
        new_device = Device(
            name=device.name,
            model=device.model,
            category_id=device.category_id,
            location_id=device.location_id,
            owner_id=device.owner_id,
            macs=database.select_all(Mac).where_in(Mac.id, device.mac_ids).all()
        )

        database.create(new_device);

        return new_device

    def update_device(self, id: int, device: DeviceInput) -> Device:
        """Update an existing device."""   
        existing_device = database.select_by_id(Device, id).first()
        if not existing_device:
            raise ValueError("Device not found")
        if not device.mac_ids:
            raise ValueError("At least one MAC address is required")

        existing_device.name = device.name
        existing_device.model = device.model
        existing_device.category_id = device.category_id
        existing_device.location_id = device.location_id
        existing_device.owner_id = device.owner_id
        existing_device.macs = database.select_all(Mac).where_in(Mac.id, device.mac_ids).all()
        
        database.update(existing_device)
        
        updated_device = database.select_by_id(Device, id).first()
        if not updated_device:
            raise ValueError("Device not found")
        
        return updated_device