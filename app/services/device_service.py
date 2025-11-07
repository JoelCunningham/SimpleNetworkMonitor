from app.common.objects import DeviceInput
from app.database.interfaces import DatabaseInterface
from app.database.models import Device, Mac
from app.services.interfaces import DeviceServiceInterface, MacServiceInterface


class DeviceService(DeviceServiceInterface):
    def __init__(self, database: DatabaseInterface, mac_service: MacServiceInterface) -> None:
        self.database = database
        self.mac_service = mac_service

    def get_devices(self,) -> list[Device]:
        devices = self.database.select(Device).all()
        macs = self.database.select(Mac).all()

        for mac in macs:
            if not any(mac.address == device_mac.address for device in devices for device_mac in device.macs):
                new_device = Device(
                    name="",
                    model="",
                    category_id=0,
                    location_id=None,
                    owner_id=None,
                    macs=[mac],
                )
                devices.append(new_device)

        return devices

    def add_device(self, device: DeviceInput) -> Device:
        new_device = Device(
            name=device.name,
            model=device.model,
            category_id=device.category_id,
            location_id=device.location_id,
            owner_id=device.owner_id,
            macs=self.database.select(Mac).where_in(Mac.id, device.mac_ids).all(),
        )

        self.database.create(new_device)
        
        database_device = self.database.select(Device).by_id(new_device.id)
        if not database_device:
            raise ValueError("Device not found")
        return database_device

    def update_device(self, id: int, device: DeviceInput) -> Device:
        existing_device = self.database.select(Device).by_id(id)
        if not existing_device:
            raise ValueError("Device not found")
        if not device.mac_ids:
            raise ValueError("At least one MAC address is required")

        existing_device.name = device.name
        existing_device.model = device.model
        existing_device.category_id = device.category_id
        existing_device.location_id = device.location_id
        existing_device.owner_id = device.owner_id
        existing_device.macs = self.database.select(Mac).where_in(Mac.id, device.mac_ids).all()

        self.database.update(existing_device)

        database_device = self.database.select(Device).by_id(id)
        if not database_device:
            raise ValueError("Device not found")
        return database_device