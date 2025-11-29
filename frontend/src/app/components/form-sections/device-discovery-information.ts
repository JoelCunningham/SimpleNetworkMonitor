import { Notification } from '#components/common';
import { BaseFormSection } from '#components/form-sections';
import { Mac, Notification as NotificationDetails } from '#interfaces';
import { NotificationType } from '#types';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-device-discovery-information',
  imports: [BaseFormSection, Notification],
  templateUrl: './device-discovery-information.html',
  styleUrl: './device-discovery-information.scss',
})
export class DeviceDiscoveryInformation {
  @Input() mac!: Mac;

  protected noDiscoveriesNotification: NotificationDetails = {
    type: NotificationType.INFO,
    message: 'No services detected',
  };
}
