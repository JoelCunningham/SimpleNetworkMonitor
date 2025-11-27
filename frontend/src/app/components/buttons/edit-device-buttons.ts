import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-edit-device-buttons',
  imports: [],
  templateUrl: './edit-device-buttons.html',
  styleUrl: './edit-device-buttons.scss',
})
export class EditDeviceButtons {
  @Input() addMode: boolean = false;

  @Output() onSubmit = new EventEmitter<void>();
  @Output() onCancel = new EventEmitter<void>();

  submit() {
    this.onSubmit.emit();
  }

  cancel() {
    this.onCancel.emit();
  }
}
