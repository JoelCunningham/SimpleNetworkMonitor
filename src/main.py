import sys

from Constants import DEFAULT_CONFIG_PATH
from Services.ServiceContainer import ServiceContainer


def main():
    """Main application entry point."""
    print("Simple Network Monitor")
    print("=" * 50)
    
    container = None
    
    try:
        container = ServiceContainer(DEFAULT_CONFIG_PATH)
        
        scanner = container.network_scanner()
        device_repo = container.device_repository()
        scan_data_repo = container.scan_data_repository()
        
        print("Scanning network...")
        
        devices = scanner.scan_network()
        
        if not devices:
            print("No devices found on the network.")
            return 0
        
        print(f"\nFound {len(devices)} devices:")
        print("-" * 80)
        
        for device in devices:
            print(f"IP: {device.ip_address}")
            
            if device.mac_address:
                print(f"  MAC: {device.mac_address}")
                
                mac_record = device_repo.save_device(device)
                scan_data_repo.save_scan_results(mac_record, device)
            
            if device.hostname:
                print(f"  Hostname: {device.hostname}")
            
            if device.mac_vendor:
                print(f"  Vendor: {device.mac_vendor}")
            
            if device.os_guess:
                print(f"  OS: {device.os_guess}")
            
            ports, services, discoveries = scanner.get_scan_summary(device)
            
            if ports:
                if len(ports) > 5:
                    ports_display = ports[:5] + [f"... +{len(ports)-5} more"]
                else:
                    ports_display = ports
                print(f"  Open Ports: {', '.join(ports_display)}")
            
            if services:
                if len(services) > 3:
                    services_display = services[:3] + [f"... +{len(services)-3} more"]
                else:
                    services_display = services
                print(f"  Services: {', '.join(services_display)}")
            
            if discoveries:
                print(f"  Discovery: {', '.join(discoveries)}")
            
            print(f"  Response Time: {device.ping_time_ms}ms")
            
            if device.arp_time_ms > 0:
                print(f"  ARP Time: {device.arp_time_ms}ms")
            
            print()
        
        print(f"Scan completed. {len(devices)} devices processed and saved to database.")
        
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    finally:
        if container:
            try:
                container.close()
            except:
                pass
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
