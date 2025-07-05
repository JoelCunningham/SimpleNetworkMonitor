from datetime import datetime, timezone
from typing import Dict, List, Optional

from sqlalchemy import Engine
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


class DeviceRepository(Injectable):
    """Repository for device data persistence."""
    
    def __init__(self, database_connection: DatabaseConnection) -> None:
        self._database_connection = database_connection
    
    def save_device(self, address_data: AddressData) -> Mac:
        """Save or update device data."""
        if address_data.mac_address is None:
            raise Exceptions.ValidationError("AddressData does not contain a MAC address.")
        
        try:
            with self._database_connection.get_session() as session:
                mac: Optional[Mac] = session.exec(
                    select(Mac).where(Mac.address == address_data.mac_address)
                ).first()

                if mac:
                    # Update existing record
                    mac.ping_time_ms = address_data.ping_time_ms
                    mac.arp_time_ms = address_data.arp_time_ms
                    mac.last_ip = address_data.ip_address
                    mac.last_seen = datetime.now(timezone.utc)      
                    mac.hostname = address_data.hostname
                    mac.vendor = address_data.mac_vendor 
                    mac.os_guess = address_data.os_guess
                    mac.ttl = address_data.ttl
                else:
                    # Create new record
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
                
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to save device: {str(e)}") from e
    
    def get_all_devices(self) -> List[Device]:
        """Get all devices from database."""
        try:
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
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to get all devices: {str(e)}") from e

class ScanDataRepository(Injectable):
    """Repository for scan data persistence."""
    
    def __init__(self, database_connection: DatabaseConnection) -> None:
        self._database_connection = database_connection
    
    def save_scan_results(self, mac: Mac, address_data: AddressData) -> None:
        """Save comprehensive scan results."""
        try:
            with self._database_connection.get_session() as session:
                # Save port data
                if address_data.open_ports:
                    self._save_port_data(session, mac, address_data.open_ports, address_data.services_info)
                
                # Save discovery data
                if address_data.discovered_info:
                    self._save_discovery_data(session, mac, address_data.discovered_info)
                
                session.commit()
                
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to save scan results: {str(e)}") from e
    
    def _save_port_data(self, session: Session, mac: Mac, port_results: List[PortInfo], 
                       service_results: Optional[Dict[int, ServiceInfo]] = None) -> None:
        """Save port scan results to the database."""
        # Remove existing port data for this MAC
        existing_ports = list(session.exec(
            select(Port).where(Port.mac_id == mac.id)
        ).all())
        for port in existing_ports:
            session.delete(port)
        
        # Add new port data
        for port_info in port_results:
            # Get service info if available
            service_name = port_info.service
            banner = getattr(port_info, 'banner', None)
            
            # Override with service detection data if available
            if service_results and port_info.port in service_results:
                service_info = service_results[port_info.port]
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
    
    def _save_discovery_data(self, session: Session, mac: Mac, discovery_results: List[DiscoveryInfo]) -> None:
        """Save discovery results to the database."""
        # Remove existing discovery data for this MAC
        existing_discoveries = list(session.exec(
            select(Discovery).where(Discovery.mac_id == mac.id)
        ).all())
        for discovery in existing_discoveries:
            # Remove associated services
            services = list(session.exec(
                select(Service).where(Service.discovery_id == discovery.id)
            ).all())
            for service in services:
                session.delete(service)
            session.delete(discovery)
        
        # Add new discovery data
        for discovery_info in discovery_results:
            discovery = Discovery(
                mac_id=mac.id,
                protocol=discovery_info.protocol,
                device_name=discovery_info.device_name,
                device_type=discovery_info.device_type,
                manufacturer=discovery_info.manufacturer,
                model=discovery_info.model
            )
            session.add(discovery)
            session.flush()  # To get the discovery.id
            
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
