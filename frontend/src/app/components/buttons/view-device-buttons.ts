import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-view-device-buttons',
  imports: [],
  templateUrl: './view-device-buttons.html',
  styleUrl: './view-device-buttons.scss',
})
export class ViewDeviceButtons {
  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.onDelete.emit();
  }
}
