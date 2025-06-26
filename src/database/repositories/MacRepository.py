from datetime import datetime, timezone
from typing import Optional

from sqlmodel import select

import Exceptions
from database.Database import Database
from database.models.MacModel import Mac
from objects.AddressData import AddressData


class MacRepository:
    
    @staticmethod
    def upsert_mac(address_data: AddressData) -> Mac:   
        if address_data.mac_address is None:
            raise Exceptions.ValidationError("AddressData does not contain a MAC address.")
        
        try:
            with Database.get_session() as session:
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
