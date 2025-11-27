import { Select } from '#components/common';
import { Device, Option } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-edit-device-buttons',
  imports: [Select],
  templateUrl: './edit-device-buttons.html',
  styleUrl: './edit-device-buttons.scss',
})
export class EditDeviceButtons {
  @Input() devices: Option<Device>[] = [];
  @Input() addMode: boolean = false;

  @Output() onSubmit = new EventEmitter<void>();
  @Output() onCancel = new EventEmitter<void>();
  @Output() onSubmitAddToDevice = new EventEmitter<Device>();

  addToExisting(device: Option<Device> | null) {
    device && this.onSubmitAddToDevice.emit(device.value);
  }

  submit() {
    this.onSubmit.emit();
  }

  cancel() {
    this.onCancel.emit();
  }
}
