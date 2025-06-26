import sys
from typing import List

import Common
import Constants
import Exceptions
from Database import Database
from Models.MacModel import Mac
from Services.MacService import MacService
from Objects.AppConfig import AppConfig
from Services.NetworkScanner import NetworkScanner


def main() -> None:
    try:
        config = AppConfig.load(Constants.DEFAULT_CONFIG_PATH)
        Database.init(config)
        scanner = NetworkScanner(config)
        
        print(f"Scanning network: {config.subnet}.{config.min_ip}-{config.max_ip}")
        address_data_list = scanner.scan_network()
        print(Constants.NETWORK_SCAN_SUMMARY.format(count=len(address_data_list)))
        
        mac_data_list: List[Mac] = []
        for address_data in address_data_list:
            if address_data.hasMac():
                try:
                    mac_data = MacService.upsert_mac(address_data)
                    mac_data_list.append(mac_data)
                except Exception as e:
                    print(f"Error processing {address_data.ip_address}: {e}")
            else:
                print(f"Skipping {address_data.ip_address} - no MAC address found.")

        print(f"\n{Constants.DEVICES_PROCESSED_SUMMARY.format(count=len(mac_data_list))}")
        print(Constants.SEPARATOR_LINE)
        for mac_data in mac_data_list:
            device_name = Common.get_device_name(mac_data.device)
            
            print(Constants.DEVICE_SCAN_FORMAT.format(
                ip=mac_data.last_ip,
                mac=mac_data.address,
                name=device_name,
                ping=mac_data.ping_time_ms,
                arp=mac_data.arp_time_ms
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
            Database.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
