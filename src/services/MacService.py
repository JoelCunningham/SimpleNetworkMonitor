from datetime import datetime, timezone
from typing import Optional

from sqlmodel import select

import Exceptions
from Models.MacModel import Mac
from Objects.AddressData import AddressData
from Objects.Injectable import Injectable
from Services.Database import Database
from Services.AdvancedDataService import AdvancedDataService


class MacService(Injectable):
    _database: Database
    _advanced_data_service: AdvancedDataService
    
    def __init__(self, database: Database, advanced_data_service: AdvancedDataService) -> None:
        self._database = database
        self._advanced_data_service = advanced_data_service
    
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
                    mac.hostname = address_data.hostname
                    mac.vendor = address_data.mac_vendor 
                    mac.os_guess = address_data.os_guess
                    mac.ttl = address_data.ttl
                else:
                    mac = Mac(
                        address=address_data.mac_address,
                        ping_time_ms=address_data.ping_time_ms,
                        arp_time_ms=address_data.arp_time_ms,
                        last_ip=address_data.ip_address,
                        hostname=address_data.hostname,
                        vendor=address_data.mac_vendor, 
                        os_guess=address_data.os_guess,
                        ttl=address_data.ttl
                    )
                    session.add(mac)

                session.commit()
                session.refresh(mac)

                # Save advanced scan data using the AdvancedDataService
                if address_data.open_ports:
                    self._advanced_data_service.save_port_data(
                        mac, 
                        address_data.open_ports, 
                        address_data.services_info
                    )
                
                if address_data.discovered_info:
                    self._advanced_data_service.save_discovery_data(mac, address_data.discovered_info)

                session.refresh(mac, attribute_names=["device"])
                if mac.device:
                    session.refresh(mac.device, attribute_names=["owner", "location", "category"])

                return mac
                
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to upsert MAC address {address_data.mac_address}: {str(e)}") from e
