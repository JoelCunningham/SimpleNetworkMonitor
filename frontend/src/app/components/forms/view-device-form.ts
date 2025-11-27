import { ViewDeviceButtons } from '#components/buttons';
import { Notification } from '#components/common';
import {
  DeviceDiscoveryInformation,
  DeviceGeneralInformation,
  DeviceNetworkInformation,
  DevicePortInformation,
} from '#components/form-sections';
import { ViewMacsGrid } from '#components/grids';
import { Device, Mac, Port } from '#interfaces';
import { DeviceService } from '#services';
import { Constants, NotificationType } from '#types';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-view-device-form',
  imports: [
    Notification,
    ViewDeviceButtons,
    ViewMacsGrid,
    DeviceGeneralInformation,
    DeviceNetworkInformation,
    DevicePortInformation,
    DeviceDiscoveryInformation,
  ],
  templateUrl: './view-device-form.html',
  styleUrl: './view-device-form.scss',
})
export class ViewDeviceForm {
  @Input() device!: Device;

  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  private currentSelectedMac: Mac | null = null;

  protected notification: string | null = null;
  protected infoNotification: NotificationType = NotificationType.INFO;
  protected errorNotification: NotificationType = NotificationType.ERROR;

  constructor(private deviceService: DeviceService) {}

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.deviceService.deleteDevice(this.device.id).subscribe({
      next: () => {
        this.onDelete.emit();
      },
      error: () => {
        this.notification = Constants.GENERIC_ERROR_MESSAGE;
      },
    });
  }

  currentMac = () => this.currentSelectedMac || this.device.primary_mac;

  selectMac(mac: Mac) {
    this.currentSelectedMac = mac;
  }

  getSortedPorts(mac: Mac | null): Port[] {
    if (!mac || !mac.ports) return [];
    return [...mac.ports].sort((a, b) => (a.number || 0) - (b.number || 0));
  }
}
