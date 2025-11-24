import { Select } from '#components/common';
import { Option, Value } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-edit-device-buttons',
  imports: [Select],
  templateUrl: './edit-device-buttons.html',
  styleUrl: './edit-device-buttons.scss',
})
export class EditDeviceButtons {
  @Input() devices: Option[] = [];
  @Input() addMode: boolean = false;

  @Output() onSubmit = new EventEmitter<Value>();
  @Output() onCancel = new EventEmitter<void>();

  addToExisting(deviceId: Value) {
    this.onSubmit.emit(deviceId);
  }

  submit() {
    this.onSubmit.emit();
  }

  cancel() {
    this.onCancel.emit();
  }
}
