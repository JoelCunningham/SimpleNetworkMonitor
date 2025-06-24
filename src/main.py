from objects.AppConfig import AppConfig
from services.DeviceResolver import DeviceResolver
from services.NetworkScanner import NetworkScanner


if __name__ == "__main__":
    config = AppConfig.load("config.json")
    resolver = DeviceResolver(config.data_file)
    scanner = NetworkScanner(config, resolver)
    devices = scanner.scan_network()
