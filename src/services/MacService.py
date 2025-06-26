from datetime import datetime, timezone
from typing import Optional

from sqlmodel import select

import Exceptions
from Models.MacModel import Mac
from Objects.AddressData import AddressData
from Objects.Injectable import Injectable
from Services.Database import Database


class MacService(Injectable):
    _database: Database
    
    def __init__(self, database: Database) -> None:
        self._database = database
    
    def upsert_mac(self, address_data: AddressData) -> Mac:   
        if address_data.mac_address is None:
            raise Exceptions.ValidationError("AddressData does not contain a MAC address.")
        
        try:
            with self._database.get_session() as session:
                mac: Optional[Mac] = session.exec(
                    select(Mac).where(Mac.address == address_data.mac_address)
                ).first()

                if mac:
                    mac.ping_time_ms = address_data.ping_time_ms
                    mac.arp_time_ms = address_data.arp_time_ms
                    mac.last_ip = address_data.ip_address
                    mac.last_seen = datetime.now(timezone.utc)
                else:
                    mac = Mac(
                        address=address_data.mac_address,
                        ping_time_ms=address_data.ping_time_ms,
                        arp_time_ms=address_data.arp_time_ms,
                        last_ip=address_data.ip_address,
                    )
                    session.add(mac)

                session.commit()

                session.refresh(mac, attribute_names=["device"])
                if mac.device:
                    session.refresh(mac.device, attribute_names=["owner", "location", "category"])

                return mac
                
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to upsert MAC address {address_data.mac_address}: {str(e)}") from e
