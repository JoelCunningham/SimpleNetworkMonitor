import { Select } from '#components/inputs/select';
import { Option, Value } from '#interfaces/option';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-add-buttons',
  imports: [Select],
  templateUrl: './add-buttons.html',
  styleUrl: './add-buttons.scss',
})
export class AddButtons {
  @Input() devices: Option[] = [];

  @Output() onAdd = new EventEmitter<void>();
  @Output() onCancel = new EventEmitter<void>();
  @Output() onSelectDevice = new EventEmitter<Value>();

  add() {
    this.onAdd.emit();
  }

  cancel() {
    this.onCancel.emit();
  }

  selectDevice(deviceId: Value) {
    this.onSelectDevice.emit(deviceId);
  }
}
