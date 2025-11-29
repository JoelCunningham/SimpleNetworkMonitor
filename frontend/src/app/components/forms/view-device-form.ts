import { ViewDeviceButtons } from '#components/buttons';
import {
  DeviceDiscoveryInformation,
  DeviceGeneralInformation,
  DeviceNetworkInformation,
  DevicePortInformation,
} from '#components/form-sections';
import { ViewMacsGrid } from '#components/grids';
import {
  Device,
  DeviceRequest,
  Mac,
  Notification,
  Option,
  Port,
} from '#interfaces';
import { DeviceService, UtilitiesService } from '#services';
import { Constants, NotificationType } from '#types';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-view-device-form',
  imports: [
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
  @Output() onSubmit = new EventEmitter<Device>();
  @Output() onDelete = new EventEmitter<void>();
  @Output() onNotification = new EventEmitter<Notification>();

  protected deviceOptions: Option<Device>[] = [];
  protected currentSelectedMac: Mac | null = null;

  constructor(
    private deviceService: DeviceService,
    private utilitiesService: UtilitiesService
  ) {}

  ngOnInit() {
    this.deviceService.currentDevices().subscribe((devices) => {
      this.deviceOptions = devices
        .map((device) => ({
          value: device,
          label: this.utilitiesService.getDisplayName(device),
        }))
        .sort((a, b) => a.label.localeCompare(b.label));
    });
  }

  edit() {
    this.onEdit.emit();
  }

  submit(device: Device) {
    const request: DeviceRequest = {
      name: device.name,
      model: device.model,
      owner_id: device.owner?.id ?? null,
      category_id: device.category?.id ?? null,
      location_id: device.location?.id ?? null,
      mac_ids: device.macs.map((mac) => mac.id),
    };

    this.deviceService.updateDevice(device.id, request).subscribe({
      next: (updatedDevice: Device) => {
        this.onSubmit.emit(updatedDevice);
        this.onNotification.emit({
          type: NotificationType.SUCCESS,
          message: 'Device updated successfully.',
        });
      },
      error: () => {
        this.onNotification.emit({
          type: NotificationType.ERROR,
          message: Constants.GENERIC_ERROR_MESSAGE,
        });
      },
    });
  }

  delete() {
    this.deviceService.deleteDevice(this.device.id).subscribe({
      next: () => {
        this.onDelete.emit();
        this.onNotification.emit({
          type: NotificationType.SUCCESS,
          message: 'Device deleted successfully.',
        });
      },
      error: () => {
        this.onNotification.emit({
          type: NotificationType.ERROR,
          message: Constants.GENERIC_ERROR_MESSAGE,
        });
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
