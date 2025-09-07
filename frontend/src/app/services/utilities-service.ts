import { Device } from '#interfaces/device';
import { HttpPort } from '#interfaces/httpPort';
import { DeviceStatus } from '#types/device-status';
import { LastSeenStatus } from '#types/last-seen-status';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class UtilitiesService {
  getLastSeenStatus(device: Device): string {
    const minsSinceLastSeen = this.getMinsSinceLastSeen(device);

    if (minsSinceLastSeen < 1) {
      return LastSeenStatus.NOW;
    } else if (minsSinceLastSeen < 60) {
      return `${Math.floor(minsSinceLastSeen)}${LastSeenStatus.MINUTE}`;
    } else if (minsSinceLastSeen < 1440) {
      return `${Math.floor(minsSinceLastSeen / 60)}${LastSeenStatus.HOUR}`;
    } else {
      return `${Math.floor(minsSinceLastSeen / 1440)}${LastSeenStatus.DAY}`;
    }
  }

  getDeviceStatus(device: Device): DeviceStatus {
    const minsSinceLastSeen = this.getMinsSinceLastSeen(device);
    if (minsSinceLastSeen < 5) {
      return DeviceStatus.ONLINE;
    } else if (minsSinceLastSeen < 10) {
      return DeviceStatus.AWAY;
    } else {
      return DeviceStatus.OFFLINE;
    }
  }

  getMinsSinceLastSeen(device: Device): number {
    const now = new Date().getTime();
    const lastSeen = new Date(device.primary_mac.last_seen).getTime();
    return (now - lastSeen) / 60000;
  }

  getDeviceHttpUrl(device: Device): string | null {
    if (!device.primary_mac || !device.primary_mac.last_ip) {
      return null;
    }

    const ip = device.primary_mac.last_ip;
    let httpPorts: HttpPort[] = [];

    if (device.macs) {
      device.macs.forEach((mac) => {
        if (mac.ports) {
          mac.ports.forEach((port) => {
            if (port) {
              const portNumber = port.port;
              const service = port.service?.toLowerCase() || '';
              if (
                [80, 443, 8080, 8443].includes(portNumber) ||
                service.includes('http')
              ) {
                httpPorts.push({
                  port: portNumber,
                  isHttps:
                    [443, 8443].includes(portNumber) ||
                    service.includes('https'),
                });
              }
            }
          });
        }
      });
    }

    if (httpPorts.length === 0) {
      return null;
    }

    // Prefer HTTP, then HTTPS, then others
    const sortedPorts = httpPorts.sort((a, b) => {
      if (!a.isHttps && b.isHttps) return -1;
      if (a.isHttps && !b.isHttps) return 1;
      if (a.port === 80) return -1;
      if (b.port === 80) return 1;
      if (a.port === 443) return -1;
      if (b.port === 443) return 1;
      return a.port - b.port;
    });

    const selectedPort = sortedPorts[0];
    const protocol = selectedPort.isHttps ? 'https' : 'http';
    const portSuffix =
      (selectedPort.port === 80 && !selectedPort.isHttps) ||
      (selectedPort.port === 443 && selectedPort.isHttps)
        ? ''
        : `:${selectedPort.port}`;

    return `${protocol}${'://'}${ip}${portSuffix}`;
  }
}
