from objects.AppConfig import AppConfig
from services.DeviceResolver import DeviceResolver
from services.NetworkScanner import NetworkScanner


if __name__ == "__main__":
    config = AppConfig.load("config.json")
    resolver = DeviceResolver(config.data_file)
    scanner = NetworkScanner(config, resolver)
    devices = scanner.scan_network()

    for device in devices:
        print(
            f"{device.ip} - {device.mac} - {device.name} | "
            f"ping: {device.ping_time_ms}ms | arp: {device.arp_time_ms}ms"
        )
