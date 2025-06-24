from objects.KnownDevice import KnownDevice
from objects.NetworkDevice import NetworkDevice


class Common:
    @staticmethod
    def get_device_name(device: NetworkDevice) -> str:
        if device.resolved:
            if KnownDevice.hasDefaultOwner(device.resolved) and device.resolved.hasNoLocation():
                return f"{device.resolved.type}"
            if KnownDevice.hasDefaultOwner(device.resolved):
                return f"{device.resolved.location} {device.resolved.type}"
            if device.resolved.hasNoLocation():
                return f"{device.resolved.owner}'s {device.resolved.type}"
            return f"{device.resolved.owner}'s {device.resolved.location} {device.resolved.type}"
        if device.mac:
            return f"Unknown device {device.mac}"
        if device.ip:
            return f"Unidentified device {device.ip}"
        return "No device information available"