from scapy.all import ARP, Ether, srp
import subprocess
import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_known_devices(filename="data.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return {}

def ping_and_arp(ip, known_devices):
    start_ping = time.time()
    result = subprocess.call(['ping', '-n', '1', '-w', '300', ip], stdout=subprocess.DEVNULL)
    ping_time = (time.time() - start_ping) * 1000

    if result != 0:
        return None

    arp = ARP(pdst=ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    start_arp = time.time()
    result = srp(packet, timeout=2, verbose=0)[0]
    arp_time = (time.time() - start_arp) * 1000

    if result:
        mac = result[0][1].hwsrc.lower()
        name = known_devices.get(mac, "Unknown")
        return {
            'ip': ip,
            'mac': mac,
            'name': name,
            'ping_time_ms': round(ping_time, 1),
            'arp_time_ms': round(arp_time, 1)
        }

    return None

if __name__ == "__main__":
    known_devices = load_known_devices("data.json")
    devices = []
    ip_range = [f"192.168.0.{i}" for i in range(1, 255)]

    with ThreadPoolExecutor(max_workers=50) as executor:
        futures = [executor.submit(ping_and_arp, ip, known_devices) for ip in ip_range]

        for future in as_completed(futures):
            device = future.result()
            if device:
                devices.append(device)
                print(f"{device['ip']} - {device['mac']} - {device['name']} | ping: {device['ping_time_ms']}ms | arp: {device['arp_time_ms']}ms")
