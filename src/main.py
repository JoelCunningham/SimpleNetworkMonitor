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
            
            if device.ttl:
                print(f"  TTL: {device.ttl}")
            
            ports, services, discoveries = scanner.get_scan_summary(device)
            
            if ports:
                if len(ports) > 5:
                    ports_display = ports[:5] + [f"... +{len(ports)-5} more"]
                else:
                    ports_display = ports
                print(f"  Open Ports: {', '.join(ports_display)}")
                
                # Show port banners if available
                if device.open_ports:
                    for port_info in device.open_ports:
                        if port_info.banner and len(port_info.banner.strip()) > 0:
                            banner_text = port_info.banner[:100] + "..." if len(port_info.banner) > 100 else port_info.banner
                            print(f"    Port {port_info.port} banner: {banner_text}")
            
            if services:
                if len(services) > 3:
                    services_display = services[:3] + [f"... +{len(services)-3} more"]
                else:
                    services_display = services
                print(f"  Services: {', '.join(services_display)}")
                
                # Show detailed service information
                if device.services_info:
                    for port, service_info in device.services_info.items():
                        details: list[str] = []
                        if service_info.version:
                            details.append(f"v{service_info.version}")
                        if service_info.product:
                            details.append(service_info.product)
                        if service_info.extra_info and len(service_info.extra_info.strip()) > 0:
                            truncated_info = service_info.extra_info[:50] + "..." if len(service_info.extra_info) > 50 else service_info.extra_info
                            details.append(truncated_info)
                        
                        if details:
                            print(f"    Port {port}: {' | '.join(details)}")
            
            if discoveries:
                print(f"  Discovery: {', '.join(discoveries)}")
                
                # Show detailed discovery information
                if device.discovered_info:
                    for discovery in device.discovered_info:
                        details: list[str] = []
                        if discovery.manufacturer:
                            details.append(f"Mfg: {discovery.manufacturer}")
                        if discovery.model:
                            details.append(f"Model: {discovery.model}")
                        if discovery.services and len(discovery.services) > 0:
                            services_list = ', '.join(discovery.services[:3])
                            details.append(f"Services: {services_list}")
                        
                        if details:
                            print(f"    {discovery.protocol.upper()}: {' | '.join(details)}")
            
            print(f"  Response Time: {device.ping_time_ms}ms")
            
            if device.arp_time_ms > 0:
                print(f"  ARP Time: {device.arp_time_ms}ms")
            
            print()
        
        print(f"Scan completed. {len(devices)} devices processed and saved to database.")
        
        # Display scan statistics
        total_ports = sum(len(device.open_ports) if device.open_ports else 0 for device in devices)
        total_services = sum(len(device.services_info) if device.services_info else 0 for device in devices)
        total_discoveries = sum(len(device.discovered_info) if device.discovered_info else 0 for device in devices)
        devices_with_hostnames = sum(1 for device in devices if device.hostname)
        devices_with_vendors = sum(1 for device in devices if device.mac_vendor)
        devices_with_os = sum(1 for device in devices if device.os_guess)
        
        print(f"\nScan Statistics:")
        print(f"  Total open ports found: {total_ports}")
        print(f"  Total services detected: {total_services}")
        print(f"  Total discovery protocols responded: {total_discoveries}")
        print(f"  Devices with hostnames: {devices_with_hostnames}")
        print(f"  Devices with vendor info: {devices_with_vendors}")
        print(f"  Devices with OS detection: {devices_with_os}")
        
        if devices:
            avg_ping_time = sum(device.ping_time_ms for device in devices) / len(devices)
            max_ping_time = max(device.ping_time_ms for device in devices)
            min_ping_time = min(device.ping_time_ms for device in devices)
            print(f"  Response time - Min: {min_ping_time}ms, Max: {max_ping_time}ms, Avg: {avg_ping_time:.1f}ms")
        
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
