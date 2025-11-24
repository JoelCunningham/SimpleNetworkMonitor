import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-owner-view-buttons',
  imports: [],
  templateUrl: './owner-view-buttons.html',
  styleUrl: './owner-view-buttons.scss',
})
export class OwnerViewButtons {
  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.onDelete.emit();
  }
}
