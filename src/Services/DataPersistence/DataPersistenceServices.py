"""Data persistence services."""
from datetime import datetime, timezone
from typing import List, Optional, Dict, Any

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine, select

import Constants
import Exceptions
from Interfaces.IConfigurationProvider import IConfigurationProvider
from Interfaces.IDataPersistence import IDatabaseConnection, IDeviceRepository, IScanDataRepository
from Models.CategoryModel import Category  # type: ignore[unused-import]
from Models.DeviceModel import Device  # type: ignore[unused-import]
from Models.LocationModel import Location  # type: ignore[unused-import]
from Models.MacModel import Mac
from Models.OwnerModel import Owner  # type: ignore[unused-import]
from Models.PortModel import Port
from Models.DiscoveryModel import Discovery
from Models.ServiceModel import Service
from Objects.AddressData import AddressData
from Objects.Injectable import Injectable
from Objects.PortInfo import PortInfo
from Objects.ServiceInfo import ServiceInfo
from Objects.DiscoveryInfo import DiscoveryInfo


class DatabaseConnection(IDatabaseConnection, Injectable):
    """Service responsible for database connection management."""
    
    def __init__(self, config_provider: IConfigurationProvider) -> None:
        self._engine: Optional[Engine] = None
        self._config_provider = config_provider
        self._initialize_database()
    
    def _initialize_database(self) -> None:
        """Initialize database connection."""
        try:
            database_path = self._config_provider.get_database_path()
            self._engine = create_engine(
                database_path,
                echo=False,
                pool_pre_ping=True,
                pool_recycle=Constants.DATABASE_POOL_RECYCLE_TIME,
            )
            
            SQLModel.metadata.create_all(self._engine)
            
        except Exception as e:
            raise Exceptions.DatabaseError(
                Constants.DB_INIT_FAILED.format(error=str(e))
            ) from e
    
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
            raise Exceptions.DatabaseError(
                Constants.DB_CLOSE_FAILED.format(error=str(e))
            ) from e


class DeviceRepository(IDeviceRepository, Injectable):
    """Repository for device data persistence."""
    
    def __init__(self, database_connection: IDatabaseConnection) -> None:
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
    
    def get_device_by_mac(self, mac_address: str) -> Optional[Mac]:
        """Get device by MAC address."""
        try:
            with self._database_connection.get_session() as session:
                return session.exec(
                    select(Mac).where(Mac.address == mac_address)
                ).first()
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to get device: {str(e)}") from e
    
    def get_all_devices(self) -> List[Mac]:
        """Get all known devices."""
        try:
            with self._database_connection.get_session() as session:
                return list(session.exec(select(Mac)).all())
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to get devices: {str(e)}") from e


class ScanDataRepository(IScanDataRepository, Injectable):
    """Repository for scan data persistence."""
    
    def __init__(self, database_connection: IDatabaseConnection) -> None:
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
    
    def get_scan_history(self, mac: Mac) -> List[Dict[str, Any]]:
        """Get scan history for device."""
        try:
            with self._database_connection.get_session() as session:
                # Get port data
                ports = list(session.exec(
                    select(Port).where(Port.mac_id == mac.id)
                ).all())
                
                # Get discovery data
                discoveries = list(session.exec(
                    select(Discovery).where(Discovery.mac_id == mac.id)
                ).all())
                
                return [
                    {
                        "ports": [{"port": p.port, "service": p.service, "protocol": p.protocol} for p in ports],
                        "discoveries": [{"protocol": d.protocol, "device_name": d.device_name, "device_type": d.device_type} for d in discoveries]
                    }
                ]
                
        except Exception as e:
            raise Exceptions.DatabaseError(f"Failed to get scan history: {str(e)}") from e
