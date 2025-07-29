from app.models.category import Category
from app.models.device import Device
from app.models.location import Location
from app.models.owner import Owner
from app.services.device_service import DeviceService


class DeviceController:
    def __init__(self, device_service: DeviceService):
        self.device_service = device_service

    def add_device(self, model: str, category_id: int, location_id: int, owner_id: int, mac_ids: list[int]) -> Device:
        return self.device_service.add_device(model, category_id, location_id, owner_id, mac_ids)

    def get_device(self, mac_address: str) -> Device | None:
        return self.device_service.get_device(mac_address);

    def get_device_locations(self) -> list[Location]:
        return self.device_service.get_device_locations()

    def get_device_categories(self) -> list[Category]:
        return self.device_service.get_device_categories()

    def get_device_owners(self) -> list[Owner]:
        return self.device_service.get_device_owners()
    
    def add_owner(self, name: str) -> Owner:
        return self.device_service.add_owner(name)