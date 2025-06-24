from typing import Optional
from database.models.DeviceModel import Device
class Common:
    
    @staticmethod
    def get_device_name(device: Optional[Device]) -> str:
        if device:
            device_name = ""
            
            device_name += device.owner.name + "'s " if device.owner else ""
            device_name += device.location.name + " " if device.location else ""
            device_name += device.category.name
            
            return device_name.strip()
        
        return "Unknown Device"
        