from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy import Engine, text
from sqlmodel import Session, SQLModel, create_engine, select

from Backend import Exceptions
from Backend.Constants import DB_POOL_RECYCLE_TIME
from Backend.Entities.CategoryModel import Category  # type: ignore[unused-import]
from Backend.Entities.DeviceModel import Device  # type: ignore[unused-import]
from Backend.Entities.DiscoveryModel import Discovery
from Backend.Entities.LocationModel import Location  # type: ignore[unused-import]
from Backend.Entities.MacModel import Mac
from Backend.Entities.OwnerModel import Owner  # type: ignore[unused-import]
from Backend.Entities.PortModel import Port
from Backend.Entities.ServiceModel import Service
from Backend.Objects.AddressData import AddressData
from Backend.Objects.DiscoveryInfo import DiscoveryInfo
from Backend.Objects.Injectable import Injectable
from Backend.Objects.PortInfo import PortInfo
from Backend.Objects.ServiceInfo import ServiceInfo
from Backend.Services.AppConfiguration import AppConfig


class DatabaseConnection(Injectable):
    """Service responsible for database connection management."""
    
    def __init__(self, config: AppConfig) -> None:
        self._engine: Optional[Engine] = None
        self._config = config
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize database connection."""
        try:
            database_path = self._config.database_path()
            self._engine = create_engine(
                database_path,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=DB_POOL_RECYCLE_TIME,
            )
            
            SQLModel.metadata.create_all(self._engine)
            
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to initialize database: {str(e)}") from e
    
    def get_session(self) -> Session:
        """Get database session."""
        if self._engine is None:
            raise Exceptions.DatabaseError("Database not initialized")
        return Session(self._engine)
    
    def close(self) -> None:
        """Close database connection."""
        try:
            if self._engine:
                self._engine.dispose()
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to close database connection: {str(e)}") from e


class DataRepository(Injectable):
    """Repository for device data persistence."""
    
    def __init__(self, database_connection: DatabaseConnection) -> None:
        self._database_connection = database_connection
    
    def save_mac_scan(self, address_data: AddressData) -> None:
        """Save or update device data for mac only scan."""
        if address_data.mac_address:
             MacRepository(self._database_connection).save_mac(address_data, True)
        
    def save_full_scan(self, address_data: AddressData) -> None:
        """Save or update device data for full scan."""
        saved_mac = None
        if address_data.mac_address:
            saved_mac = MacRepository(self._database_connection).save_mac(address_data, False)
        if saved_mac and address_data.open_ports:
            PortRepository(self._database_connection).save_port(saved_mac, address_data.open_ports, address_data.services_info)      
        if saved_mac and address_data.discovered_info:
            DiscoveryRepository(self._database_connection).save_discoveries(saved_mac, address_data.discovered_info)
        
    
    def get_latest_scan_date(self) -> Optional[datetime]:
        """Get the date of the latest scan."""
        with self._database_connection.get_session() as session:
            latest_scan = session.exec(
                select(Mac).order_by(text("last_seen DESC"))
            ).first()
            
            if latest_scan:
                return latest_scan.last_seen
            
            return None
    
    def get_all_devices(self) -> List[Device]:
        """Get all devices from database."""
        with self._database_connection.get_session() as session:
            devices = list(session.exec(select(Device)).all())
            
            # Manually load relationships for each device
            for device in devices:
                _ = device.macs 
                _ = device.category  
                _ = device.owner
                _ = device.location
                for mac in device.macs:
                    _ = mac.discoveries
                    _ = mac.ports
                    for discovery in mac.discoveries:
                        _ = discovery.services
            
            return devices

    def get_known_unknown_devices(self, scanned_devices: List[AddressData]) -> List[Device]:
        """Get all devices from database."""
        
        devices = self.get_all_devices()
            
        for device_data in scanned_devices:
            if device_data.mac_address:
                # Check if the scanned MAC matches ANY MAC associated with existing devices
                has_device = next((d for d in devices if any(mac.address == device_data.mac_address for mac in d.macs)), None)
                
                if not has_device:
                    mac_data = MacRepository(self._database_connection).get_mac_by_address(device_data.mac_address)
                    
                    if mac_data:
                        devices.append(Device(
                            macs=[mac_data],
                            category_id=0
                        ))
        
        return devices

class MacRepository(Injectable):
    
    def __init__(self, database_connection: DatabaseConnection) -> None:
        self._database_connection = database_connection

    def save_mac(self, address_data: AddressData, preserve: bool = False) -> Mac:
        """Save or update MAC address data."""
        if address_data.mac_address is None:
            raise Exceptions.ValidationError("AddressData does not contain a MAC address.")
    
        with self._database_connection.get_session() as session:
            mac: Optional[Mac] = session.exec(
                select(Mac).where(Mac.address == address_data.mac_address)
            ).first()

            if mac:
                mac.ping_time_ms = address_data.ping_time_ms
                mac.arp_time_ms = address_data.arp_time_ms
                mac.last_ip = address_data.ip_address
                mac.last_seen = datetime.now(timezone.utc)
                
                if preserve:
                    mac.hostname = address_data.hostname or mac.hostname
                    mac.vendor = address_data.mac_vendor or mac.vendor
                    mac.os_guess = address_data.os_guess or mac.os_guess
                    mac.ttl = address_data.ttl or mac.ttl
                else:
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
                    ttl=address_data.ttl,
                    last_seen=datetime.now(timezone.utc)
                )
                session.add(mac)

            session.commit()
            session.refresh(mac)
            return mac
    
    
    def get_mac_by_address(self, mac_address: str) -> Optional[Mac]:
        with self._database_connection.get_session() as session:
            mac = session.exec(
                select(Mac).where(Mac.address == mac_address)
            ).first()
            
            # Manually load relationships for the MAC
            if mac:
                _ = mac.discoveries
                _ = mac.ports
                for discovery in mac.discoveries:
                    _ = discovery.services
                        
            return mac

class PortRepository(Injectable):
    """Repository for port data persistence."""
    
    def __init__(self, database_connection: DatabaseConnection) -> None:
        self._database_connection = database_connection

    def save_port(self, mac: Mac, ports: List[PortInfo], services: Optional[Dict[int, ServiceInfo]]) -> None:
        if not ports:
            raise Exceptions.ValidationError("AddressData does not contain open ports.")

        with self._database_connection.get_session() as session:
            # Remove existing port data for this MAC
            existing_ports = list(session.exec(
                select(Port).where(Port.mac_id == mac.id)
            ).all())
            for port in existing_ports:
                session.delete(port)
            
            for port_info in ports:
                service_name = port_info.service
                banner = getattr(port_info, 'banner', None)
                
                # Override with service detection data if available
                if services and port_info.port in services:
                    service_info = services[port_info.port]
                    if service_info.service_name:
                        service_name = service_info.service_name
                        if service_info.version:
                            service_name += f" {service_info.version}"
                
                port = Port(
                    mac_id=mac.id,
                    port=port_info.port,
                    protocol=port_info.protocol,
                    service=service_name,
                    banner=banner
                )
                session.add(port)
            
            session.commit()
                
class DiscoveryRepository(Injectable):
    
    def __init__(self, database_connection: DatabaseConnection) -> None:
        self._database_connection = database_connection

    def save_discoveries(self, mac: Mac, discoveries: List[DiscoveryInfo]) -> None:
        if not discoveries:
            raise Exceptions.ValidationError("AddressData does not contain discovery information.")

        with self._database_connection.get_session() as session:
            # Remove existing discovery data for this MAC
            existing_discoveries = list(session.exec(
                select(Discovery).where(Discovery.mac_id == mac.id)
            ).all())
            for discovery in existing_discoveries:
                services = list(session.exec(
                    select(Service).where(Service.discovery_id == discovery.id)
                ).all())
                for service in services:
                    session.delete(service)
                session.delete(discovery)
            
            # Add new discovery data
            for discovery_info in discoveries:
                discovery = Discovery(
                    mac_id=mac.id,
                    protocol=discovery_info.protocol,
                    device_name=discovery_info.device_name,
                    device_type=discovery_info.device_type,
                    manufacturer=discovery_info.manufacturer,
                    model=discovery_info.model
                )
                session.add(discovery)
                session.flush()
                
                # Add services if any
                if discovery_info.services:
                    for service_name in discovery_info.services:
                        service = Service(
                            discovery_id=discovery.id,
                            name=service_name,
                            version=None,
                            port=None
                        )
                        session.add(service)
                        
            session.commit()
