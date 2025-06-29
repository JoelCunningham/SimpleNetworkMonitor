import sys
from typing import List, Dict

import Common
import Constants
import Exceptions
from Container import Container
from Models.MacModel import Mac
from Services.AdvancedDataService import AdvancedDataService

def get_advanced_scan_summary(mac: Mac, advanced_data_service: AdvancedDataService) -> Dict[str, str]:
    """Get a summary of advanced scan results for display."""
    summary = {
        "ports": "",
        "services": ""
    }
    
    try:
        # Get port data
        ports = advanced_data_service.get_port_data(mac)
        if ports:
            port_numbers = [str(port.port) for port in ports[:3]]  # Show first 3 ports
            summary["ports"] = ",".join(port_numbers)
            if len(ports) > 3:
                summary["ports"] += f"+{len(ports)-3}"
        
        # Get service data from ports
        port_services = [port.service for port in ports if port.service]
        
        # Get service data from discovery
        discoveries = advanced_data_service.get_discovery_data(mac)
        discovery_services: List[str] = []
        for discovery in discoveries:
            for service in discovery.services:
                discovery_services.append(service.name)
        
        # Combine all services
        all_services = port_services + discovery_services
        if all_services:
            service_names = all_services[:2]  # Show first 2 services
            summary["services"] = ",".join(service_names)
            if len(all_services) > 2:
                summary["services"] += f"+{len(all_services)-2}"
    
    except Exception:
        summary["ports"] = "Error"
        summary["services"] = "Error"
    
    return summary


def main() -> None:
    container = Container()
    
    app_config = container.config.get()    
    scanner_service = container.scanner_service.get()
    mac_service = container.mac_service.get()
    advanced_data_service = container.advanced_data_service.get()
    
    try:
        print(f"Scanning network: {app_config.subnet}.{app_config.min_ip}-{app_config.max_ip}")
        address_data_list = scanner_service.scan_network()
        print(Constants.NETWORK_SCAN_SUMMARY.format(count=len(address_data_list)))
        
        mac_data_list: List[Mac] = []
        for address_data in address_data_list:
            if address_data.hasMac():
                try:
                    mac_data = mac_service.upsert_mac(address_data)
                    mac_data_list.append(mac_data)
                except Exception as e:
                    print(f"Error processing {address_data.ip_address}: {e}")
            else:
                print(f"Skipping {address_data.ip_address} - no MAC address found.")

        print(f"\n{Constants.DEVICES_PROCESSED_SUMMARY.format(count=len(mac_data_list))}")
        print(Constants.SEPARATOR_LINE)
        for mac_data in mac_data_list:
            device_name = Common.get_device_name(mac_data.device)
            
            try:
                ports = advanced_data_service.get_port_data(mac_data)
                discoveries = advanced_data_service.get_discovery_data(mac_data)
                has_advanced_data = len(ports) > 0 or len(discoveries) > 0
            except Exception:
                has_advanced_data = False
            
            if has_advanced_data:
                scan_summary = get_advanced_scan_summary(mac_data, advanced_data_service)
                
                print(Constants.DEVICE_SCAN_FORMAT_ADVANCED.format(
                    ip=mac_data.last_ip,
                    mac=mac_data.address,
                    name=device_name,
                    ping=mac_data.ping_time_ms,
                    arp=mac_data.arp_time_ms,
                    hostname=mac_data.hostname or "Unknown",
                    vendor=mac_data.vendor or "Unknown", 
                    os_guess=mac_data.os_guess or "Unknown",
                    ports=scan_summary["ports"] or "None",
                    services=scan_summary["services"] or "None"
                ))
            else:
                print(Constants.DEVICE_SCAN_FORMAT.format(
                    ip=mac_data.last_ip,
                    mac=mac_data.address,
                    name=device_name,
                    ping=mac_data.ping_time_ms,
                    arp=mac_data.arp_time_ms,
                    hostname=mac_data.hostname or "Unknown",
                    vendor=mac_data.vendor or "Unknown", 
                    os_guess=mac_data.os_guess or "Unknown"
                ))

    except KeyboardInterrupt:
        print(Constants.SCAN_INTERRUPTED_MESSAGE)
        sys.exit(Constants.EXIT_FAILURE)
    except (Exceptions.ConfigurationError, Exceptions.DatabaseError, Exceptions.NetworkScanError) as e:
        print(f"Error: {e}")
        sys.exit(Constants.EXIT_FAILURE)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(Constants.EXIT_FAILURE)
    finally:
        try:
            container.dispose()  
        except Exception:
            pass


if __name__ == "__main__":
    main()
