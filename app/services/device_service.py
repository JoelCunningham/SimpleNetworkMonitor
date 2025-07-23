from app import database
from app.models.device import Device
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
