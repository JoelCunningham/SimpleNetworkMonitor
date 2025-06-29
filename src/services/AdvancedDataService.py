from typing import Dict, List, Optional

from sqlmodel import select

from Models.DiscoveryModel import Discovery
from Models.MacModel import Mac
from Models.PortModel import Port
from Models.ServiceModel import Service
from Objects.DiscoveryInfo import DiscoveryInfo
from Objects.Injectable import Injectable
from Objects.PortInfo import PortInfo
from Objects.ServiceInfo import ServiceInfo
from Services.Database import Database


class AdvancedDataService(Injectable):
    """Service for managing advanced scan data relationships in the database."""
    
    def __init__(self, database: Database) -> None:
        self._database = database
    
    def save_port_data(self, mac: Mac, port_results: List[PortInfo], service_results: Optional[Dict[int, ServiceInfo]] = None) -> None:
        """Save port scan results to the database."""
        if not port_results:
            return
            
        try:
            with self._database.get_session() as session:
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
                    banner = port_info.banner
                    
                    # Override with service detection data if available
                    if service_results and port_info.port in service_results:
                        service_info = service_results[port_info.port]
                        if service_info.service_name:
                            service_name = service_info.service_name
                            if service_info.version:
                                service_name += f" {service_info.version}"
                    
                    port = Port(
                        port=port_info.port,
                        protocol=port_info.protocol,
                        service=service_name,
                        banner=banner,
                        state=port_info.state,
                        mac_id=mac.id
                    )
                    session.add(port)
                
                session.commit()
                
        except Exception as e:
            raise Exception(f"Failed to save port data for MAC {mac.address}: {str(e)}") from e
    
    def save_discovery_data(self, mac: Mac, discovery_results: List[DiscoveryInfo]) -> None:
        """Save discovery results to the database."""
        if not discovery_results:
            return
            
        try:
            with self._database.get_session() as session:
                # Remove existing discovery data for this MAC
                existing_discoveries = list(session.exec(
                    select(Discovery).where(Discovery.mac_id == mac.id)
                ).all())
                for discovery in existing_discoveries:
                    session.delete(discovery)
                
                # Add new discovery data
                for discovery_info in discovery_results:
                    discovery = Discovery(
                        protocol=discovery_info.protocol,
                        device_name=discovery_info.device_name,
                        device_type=discovery_info.device_type,
                        manufacturer=discovery_info.manufacturer,
                        model=discovery_info.model,
                        mac_id=mac.id
                    )
                    session.add(discovery)
                    session.flush()  # Get the discovery ID
                    
                    # Add services if present
                    if discovery_info.services:
                        for service_name in discovery_info.services:
                            service = Service(
                                name=service_name,
                                protocol=discovery_info.protocol,
                                discovery_id=discovery.id
                            )
                            session.add(service)
                
                session.commit()
                
        except Exception as e:
            raise Exception(f"Failed to save discovery data for MAC {mac.address}: {str(e)}") from e
    
    def get_port_data(self, mac: Mac) -> List[Port]:
        """Get port scan results for a MAC address."""
        try:
            with self._database.get_session() as session:
                return list(session.exec(
                    select(Port).where(Port.mac_id == mac.id)
                ).all())
        except Exception as e:
            raise Exception(f"Failed to get port data for MAC {mac.address}: {str(e)}") from e
    
    def get_discovery_data(self, mac: Mac) -> List[Discovery]:
        """Get discovery results for a MAC address."""
        try:
            with self._database.get_session() as session:
                return list(session.exec(
                    select(Discovery).where(Discovery.mac_id == mac.id)
                ).all())
        except Exception as e:
            raise Exception(f"Failed to get discovery data for MAC {mac.address}: {str(e)}") from e
