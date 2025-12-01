import { Device, PortInfo, Port } from '#interfaces';
import { DeviceStatus, LastSeenStatus } from '#types';
import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class UtilitiesService {
  defaultDeviceName = 'Unknown Device';

  getDisplayName(device: Device | null): string {
    if (!device) return this.defaultDeviceName;
    if (device.name) return device.name;

    const displayName = this.getDisplayNameEx(
      device?.owner?.name || '',
      device?.location?.name || '',
      device?.category?.name || ''
    );

    if (displayName == this.defaultDeviceName) {
      return this.defaultDeviceName + ' ' + device.primary_mac.address;
    }
    return displayName;
  }

  getDisplayNameEx(owner: string, location: string, category: string): string {
    let displayName = '';
    displayName += owner ? owner + "'s " : '';
    displayName += location ? location + ' ' : '';
    displayName += category ? category : '';

    return displayName.trim() || this.defaultDeviceName;
  }

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

  httpPortNumbers = [80, 443];
  httpsPortNumber = 443;

  getDeviceHttpUrl(device: Device): string | undefined {
    if (!device.primary_mac || !device.primary_mac.last_ip) {
      return undefined;
    }

    const ip = device.primary_mac.last_ip;
    const httpPorts = device.macs
      .flatMap((mac) => mac.ports || [])
      .filter((port) => this.httpPortNumbers.includes(port.number))
      .sort((a, b) => a.number - b.number);

    if (httpPorts.length === 0) {
      return undefined;
    }

    return this.getPortHttpUrl(ip, httpPorts[0].number);
  }

  getPortHttpUrl(ip: string, port: number): string | undefined {
    if (this.httpPortNumbers.includes(port)) {
      const protocol = port === this.httpsPortNumber ? 'https' : 'http';
      return `${protocol}${'://'}${ip}:${port}`;
    }
    return undefined;
  }

  sortDevices(devices: Device[]): Device[] {
    return devices.sort((a, b) => {
      const aLatestMac = this.getLatestMacTime(a);
      const bLatestMac = this.getLatestMacTime(b);
      if (bLatestMac !== aLatestMac) return bLatestMac - aLatestMac;
      return (a.macs[0]?.hostname || '').localeCompare(
        b.macs[0]?.hostname || ''
      );
    });
  }

  getPortInfo(ip: string, ports: Port[]): PortInfo[] {
    return ports
      .map((port) => ({
        port: port,
        isHttp: this.httpPortNumbers.includes(port.number),
        address: this.getPortHttpUrl(ip, port.number),
      }))
      .sort((a, b) => {
        return a.port.number - b.port.number;
      });
  }

  getLatestMacTime(device: Device): number {
    return device.macs
      .map((mac) => (mac.last_seen ? new Date(mac.last_seen).getTime() : 0))
      .reduce((max, current) => Math.max(max, current), 0);
  }
}
