import { Select } from '#components/common';
import { Device, Option } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-view-device-buttons',
  imports: [Select],
  templateUrl: './view-device-buttons.html',
  styleUrl: './view-device-buttons.scss',
})
export class ViewDeviceButtons {
  @Input() devices: Option<Device>[] = [];
  @Input() addMode: boolean = false;

  @Output() onAdd = new EventEmitter<void>();
  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();
  @Output() onSubmitAddToDevice = new EventEmitter<Device>();

  add() {
    this.onAdd.emit();
  }

  addToExisting(device: Option<Device> | null) {
    device && this.onSubmitAddToDevice.emit(device.value);
  }

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.onDelete.emit();
  }
}
