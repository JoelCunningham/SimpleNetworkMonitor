from datetime import datetime, timezone 
from sqlmodel import select

from database.Database import Database
from database.models.MacModel import Mac
from objects.AddressData import AddressData


class MacRepository:
    
    @staticmethod
    def upsert_mac(addressData: AddressData) -> Mac:   
        if addressData.mac is None:
            raise ValueError("AddressData does not contain a MAC address.")
        
        with Database.get_session() as session:
            mac = session.exec(select(Mac).where(Mac.address == addressData.mac)).first()

            if mac:
                mac.ping_time_ms = addressData.ping_time_ms
                mac.arp_time_ms = addressData.arp_time_ms
                mac.last_ip = addressData.ip
                mac.last_seen = datetime.now(timezone.utc)
            else:
                mac = Mac(
                    address=addressData.mac,
                    ping_time_ms=addressData.ping_time_ms,
                    arp_time_ms=addressData.arp_time_ms,
                    last_ip=addressData.ip,
                    last_seen=datetime.now(timezone.utc)
                )
                session.add(mac)

            session.commit()

            session.refresh(mac, attribute_names=["device"])
            if mac.device:
                session.refresh(mac.device, attribute_names=["owner", "location", "category"])

            return mac
