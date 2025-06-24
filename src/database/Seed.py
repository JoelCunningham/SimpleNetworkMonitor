from datetime import datetime, timezone
from typing import Dict, Optional, Type, TypeVar

from sqlmodel import select, Session

from database.Database import Database
from database.models.MacModel import Mac # type: ignore[unused-import]
from database.models.DeviceModel import Device # type: ignore[unused-import]
from database.models.OwnerModel import Owner # type: ignore[unused-import]
from database.models.LocationModel import Location # type: ignore[unused-import]
from database.models.CategoryModel import Category  # type: ignore[unused-import]

T = TypeVar("T")


DATA: Dict[str, Dict[str, str | list[str]]] = {
  "router": {
    "macs": ["48:d2:4f:26:7a:4e"],
    "type": "Router",
    "owner": "Household",
    "location": "None",
    "model": "Sagemcom F@ST 5366 TN"
  },
  "printer": {
    "macs": ["40:b0:34:76:ba:a4"],
    "type": "Printer",
    "owner": "Household",
    "location": "None",
    "model": "HP OfficeJet Pro 7740"
  },
  "nvr": {
    "macs": ["b2:be:76:af:c8:9d"],
    "type": "NVR",
    "owner": "Household",
    "location": "None",
    "model": "Dahua NVR4108HS-8P-4KS2/L"
  },
  "joel_laptop": {
    "macs": ["f4:a8:0d:2f:35:d8", "64:79:f0:4b:cc:a6"],
    "type": "Laptop",
    "owner": "Joel",
    "location": "None",
    "model": "HP Envy 14"
  },
  "joel_google_home": {
    "macs": ["38:8b:59:4f:f0:ce"],
    "type": "Smart Speaker",
    "owner": "Joel",
    "location": "Bedroom",
    "model": "Google Home Mini"
  },
  "kitchen_google_home": {
    "macs": ["b2:be:76:ed:74:b3"],
    "type": "Smart Speaker",
    "owner": "Household",
    "location": "Kitchen",
    "model": "Google Home Mini"
  },
  "living_tv": {
    "macs": ["b2:be:76:4c:07:55"],
    "type": "Smart TV",
    "owner": "Household",
    "location": "Living",
    "model": "Panasonic VIErA TH-75FX780A"
  },
  "joel_phone": {
    "macs": ["7a:46:af:82:0a:1e"],
    "type": "Smart Phone",
    "owner": "Joel",
    "location": "None",
    "model": "Samsung Galaxy S21 FE"
  },
  "caryn_tablet": {
    "macs": ["3a:c2:11:94:93:f3"],
    "type": "Tablet",
    "owner": "Caryn",
    "location": "None",
    "model": "iPad Air 2"
  },
  "caryn_desktop": {
    "macs": ["2c:f0:5d:22:28:3c"],
    "type": "Desktop",
    "owner": "Caryn",
    "location": "None",
    "model": "None"
  },
  "rumpus_tv": {
    "macs": ["a8:a6:48:41:f1:ac"],
    "type": "Smart TV",
    "owner": "Household",
    "location": "Rumpus",
    "model": "TBD"
  },
  "ruth_desktop": {
    "macs": ["18:c0:4d:34:2d:e1"],
    "type": "Desktop",
    "owner": "Ruth",
    "location": "None",
    "model": "None"
  },
  "kitchen_radio": {
    "macs": ["b2:be:76:e3:3c:ad"],
    "type": "Smart Radio",
    "owner": "Household",
    "location": "Kitchen",
    "model": "Tivoli Model One Digital"
  },
  "joel_desktop": {
    "macs": ["2c:f0:5d:08:9c:fb"],
    "type": "Desktop",
    "owner": "Joel",
    "location": "None",
    "model": "None"
  },
  "bridge": {
    "macs": ["b2:be:76:d2:a1:26"],
    "type": "Bridge",
    "owner": "Household",
    "location": "Hallway",
    "model": "TP-LINK TL-WR840N"
  },
  "caryn_phone": {
    "macs": ["36:c2:0d:f1:b8:b2"],
    "type": "Smart Phone",
    "owner": "Caryn",
    "location": "None",
    "model": "Google Pixel 7"
  }
}

def get_or_create(
    session: Session,
    model_cls: Type[T],
    key_field_name: str,
    value: str
) -> T:
    statement = select(model_cls).where(getattr(model_cls, key_field_name) == value)
    instance = session.exec(statement).first()
    if instance is not None:
        return instance
    instance = model_cls(**{key_field_name: value})  # type: ignore
    session.add(instance)
    session.commit()
    session.refresh(instance)
    return instance


def seed() -> None:
    with Database.get_session() as session:
        for _device_key, data in DATA.items():
            if (isinstance(data["owner"], str) and
                isinstance(data["location"], str) and 
                isinstance(data["type"], str) and
                isinstance(data["model"], str) and
                isinstance(data["macs"], list)):
                
                owner: Owner = get_or_create(session, Owner, "name", data["owner"])
                location: Location = get_or_create(session, Location, "name", data["location"])
                category: Category = get_or_create(session, Category, "name", data["type"])

                # Find existing device by model & owner_id (adjust fields if needed)
                statement = select(Device).where(
                    (Device.model == data["model"]) &
                    (Device.owner_id == owner.id)
                )
                device: Optional[Device] = session.exec(statement).first()

                if device is None:
                    device = Device(
                        model=data["model"],
                        owner_id=owner.id,
                        location_id=location.id,
                        category_id=category.id,
                    )
                    session.add(device)
                    session.commit()
                    session.refresh(device)

                for mac_addr in data["macs"]:
                    mac_stmt = select(Mac).where(Mac.address == mac_addr)
                    mac: Optional[Mac] = session.exec(mac_stmt).first()
                    if mac is None:
                        mac = Mac(
                            address=mac_addr,
                            ping_time_ms=0,
                            arp_time_ms=0,
                            last_ip="",
                            last_seen=datetime.now(timezone.utc),
                            device_id=device.id
                        )
                        session.add(mac)
                session.commit()


if __name__ == "__main__":
    seed()
    print("Database seeded successfully!")
