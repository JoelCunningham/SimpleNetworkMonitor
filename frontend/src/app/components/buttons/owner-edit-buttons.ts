import { Select } from '#components/common';
import { Device, Option } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-owner-edit-buttons',
  imports: [Select],
  templateUrl: './owner-edit-buttons.html',
  styleUrl: './owner-edit-buttons.scss',
})
export class OwnerEditButtons {
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

  selectDevice(device: Option<Device> | null) {
    device && this.onSelectDevice.emit(device.value);
  }
}
