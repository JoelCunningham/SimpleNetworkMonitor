import { DeviceCard } from '#components/cards';
import { Device, Owner } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-edit-devices-grid',
  imports: [DeviceCard],
  templateUrl: './edit-devices-grid.html',
  styleUrl: './edit-devices-grid.scss',
})
export class EditDevicesGrid {
  @Input() owner!: Owner;

  @Output() onRemoveDevice = new EventEmitter<Device>();

  removeDevice(device: Device) {
    this.onRemoveDevice.emit(device);
  }
}
