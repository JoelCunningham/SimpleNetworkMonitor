import { Select } from '#components/common/select';
import { Option, Value } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-edit-buttons',
  imports: [Select],
  templateUrl: './edit-buttons.html',
  styleUrl: './edit-buttons.scss',
})
export class EditButtons {
  @Input() devices: Option[] = [];
  @Input() addMode: boolean = false;

  @Output() onSubmit = new EventEmitter<void>();
  @Output() onCancel = new EventEmitter<void>();
  @Output() onSelectDevice = new EventEmitter<Value>();

  save() {
    this.onSubmit.emit();
  }

  cancel() {
    this.onCancel.emit();
  }

  selectDevice(deviceId: Value) {
    this.onSelectDevice.emit(deviceId);
  }
}
