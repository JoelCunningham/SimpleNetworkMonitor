import { Select } from '#components/common';
import { Device, Option } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-edit-owner-buttons',
  imports: [Select],
  templateUrl: './edit-owner-buttons.html',
  styleUrl: './edit-owner-buttons.scss',
})
export class EditOwnerButtons {
  @Input() devices: Option<Device>[] = [];
  @Input() addMode: boolean = false;

  @Output() onSubmit = new EventEmitter<void>();
  @Output() onCancel = new EventEmitter<void>();
  @Output() onSelectDevice = new EventEmitter<Device>();

  submit() {
    this.onSubmit.emit();
  }

  cancel() {
    this.onCancel.emit();
  }

  selectDevice() {
    const selectedDevice = this.devices.find((device) => device.selected);
    if (selectedDevice) {
      this.onSelectDevice.emit(selectedDevice.value);
    }
  }
}
