import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-view-buttons',
  imports: [],
  templateUrl: './view-buttons.html',
  styleUrl: './view-buttons.scss',
})
export class ViewButtons {
  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.onDelete.emit();
  }
}
