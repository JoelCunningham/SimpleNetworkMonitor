from objects.AppConfig import AppConfig
from services.DeviceResolver import DeviceResolver
from services.NetworkScanner import NetworkScanner
from utilities.Common import Common


def main():
    APP_CONFIG_FILE = "config.json"
    config = AppConfig.load(APP_CONFIG_FILE)
    
    Resolver = DeviceResolver(config.data_file)
    Scanner = NetworkScanner(config, Resolver)
    
    devices = Scanner.scan_network()

    for device in devices:
        device_name = Common.get_device_name(device)
        print(
            f"{device.ip} - {device.mac} - {device_name} | "
            f"ping: {device.ping_time_ms}ms | arp: {device.arp_time_ms}ms"
        )

if __name__ == "__main__":
    main()
