from objects.NetworkDevice import NetworkDevice

class Common:
    
    @staticmethod
    def get_device_name(device: NetworkDevice) -> str:
        device_name = ""
        
        if device.resolved:
            details = device.resolved

            device_name += details.owner + "'s " if not details.hasDefaultOwner() else ""
            device_name += details.location + " " if not details.hasNoLocation() else ""
            device_name += details.type + " "

            return device_name.strip()
        
        if device.mac:
            return f"Unknown device {device.mac}"
        if device.ip:
            return f"Unidentified device {device.ip}"
        return "No device information available"