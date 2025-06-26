from typing import Optional

import Constants
from database.models.DeviceModel import Device


def get_device_name(device: Optional[Device]) -> str:
    if device:
        device_name = ""
        
        device_name += device.owner.name + "'s " if device.owner else ""
        device_name += device.location.name + " " if device.location else ""
        device_name += device.category.name
        
        return device_name.strip()
    
    return Constants.UNKNOWN_DEVICE_NAME
        