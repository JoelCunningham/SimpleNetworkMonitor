import { Icon, Notification } from '#components/common';
import { BaseFormSection } from '#components/form-sections';
import {
  Notification as NotificationDetails,
  Port,
  PortInfo,
} from '#interfaces';
import { UtilitiesService } from '#services';
import { NotificationType } from '#types';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-device-port-information',
  imports: [BaseFormSection, Icon, Notification],
  templateUrl: './device-port-information.html',
  styleUrl: './device-port-information.scss',
})
export class DevicePortInformation {
  @Input() ports: Port[] = [];
  @Input() deviceIp: string = '';

  protected noPortsNotification: NotificationDetails = {
    type: NotificationType.INFO,
    message: 'No open ports detected',
  };

  constructor(private utilitiesService: UtilitiesService) {}

  getSortedPorts(): PortInfo[] {
    return this.utilitiesService.getPortInfo(this.deviceIp, this.ports);
  }

  getPortDescription(info: PortInfo): string {
    const service = info.port.service ? ` (${info.port.service})` : '';
    return `${info.port.number}${service}`;
  }
}
