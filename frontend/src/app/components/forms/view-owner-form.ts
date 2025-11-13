import { ViewButtons } from '#components/buttons/view-buttons';
import { Notification } from '#components/common/notification';
import { ViewField } from '#components/fields/view-field';
import { Owner } from '#interfaces';
import { OwnerService } from '#services/owner-service';
import { NotificationType } from '#types/notification-type';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ViewDevicesGrid } from '../grids/view-devices-grid';

@Component({
  standalone: true,
  selector: 'app-view-owner-form',
  imports: [ViewField, ViewDevicesGrid, ViewButtons, Notification],
  templateUrl: './view-owner-form.html',
  styleUrl: './view-owner-form.scss',
})
export class ViewOwnerForm {
  @Input() owner!: Owner;

  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  protected notification: string | null = null;
  protected errorNotification: NotificationType = NotificationType.ERROR;

  constructor(private ownerService: OwnerService) {}

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.ownerService.deleteOwner(this.owner.id).subscribe({
      next: () => {
        this.onDelete.emit();
      },
      error: () => {
        this.notification = 'An unexpected error occurred. Please try again.';
      },
    });
  }
}
