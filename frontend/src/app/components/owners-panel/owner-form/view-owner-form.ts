import { ViewField } from '#components/common/view-field';
import { Owner } from '#interfaces/owner';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ViewButtons } from './view-buttons';
import { ViewDevicesGrid } from './view-devices-grid';

@Component({
  standalone: true,
  selector: 'app-view-owner-form',
  imports: [ViewField, ViewDevicesGrid, ViewButtons],
  templateUrl: './view-owner-form.html',
  styleUrl: './view-owner-form.scss',
})
export class ViewOwnerForm {
  @Input() owner!: Owner;

  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.onDelete.emit();
  }
}
