from database.Database import Database
from database.models.MacModel import Mac
from database.repositories.MacRepository import MacRepository
from objects.AppConfig import AppConfig
from services.NetworkScanner import NetworkScanner
from utilities.Common import Common


def main():
    config = AppConfig.load("config.json")

    Database.init()
    Scanner = NetworkScanner(config)
    
    addresses_data = Scanner.scan_network()
    macs_data: list[Mac] = []

    for address_data in addresses_data:
        if address_data.hasMac():
           macs_data.append(MacRepository.upsert_mac(address_data))
        else:
           print(f"Skipping {address_data.ip} - no MAC address found.")

    for macData in macs_data:
        device_name = Common.get_device_name(macData.device)
        
        print(
            f"{macData.last_ip} - {macData.address} - {device_name} | "
            f"ping: {macData.ping_time_ms}ms | arp: {macData.arp_time_ms}ms"
        )

if __name__ == "__main__":
    main()
