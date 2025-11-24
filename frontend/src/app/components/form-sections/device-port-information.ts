import { Icon, Notification } from '#components/common';
import { BaseFormSection } from '#components/form-sections';
import { Port } from '#interfaces';
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

  protected infoNotification: NotificationType = NotificationType.INFO;
  protected portUrls: { [key: number]: string | null } = {};

  constructor(private utilitiesService: UtilitiesService) {}

  getPortUrl(port: Port): string | null {
    if (!this.portUrls[port.number]) {
      this.portUrls[port.number] = this.utilitiesService.getPortHttpUrl(
        this.deviceIp,
        port.number
      );
    }
    return this.portUrls[port.number];
  }

  getPortDescription(port: Port) {
    const service = port.service ? ` (${port.service.split(' ')[0]})` : '';
    return `${port.number}${service}`;
  }
}
