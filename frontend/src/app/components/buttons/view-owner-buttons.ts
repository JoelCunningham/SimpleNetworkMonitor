import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-view-owner-buttons',
  imports: [],
  templateUrl: './view-owner-buttons.html',
  styleUrl: './view-owner-buttons.scss',
})
export class ViewOwnerButtons {
  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.onDelete.emit();
  }
}
