from app.services.device_service import DeviceService


class DeviceController:
    def __init__(self, device_service: DeviceService):
        self.device_service = device_service

    def get_device_locations(self):
        return self.device_service.get_device_locations()

    def get_device_categories(self):
        return self.device_service.get_device_categories()
    
    def get_device_owners(self):
        return self.device_service.get_device_owners()