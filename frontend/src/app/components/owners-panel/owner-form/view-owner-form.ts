import { ViewField } from '#components/common/view-field';
import { Owner } from '#interfaces/owner';
import { OwnerService } from '#services/owner-service';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { ViewButtons } from './view-buttons';
import { ViewDevicesGrid } from './view-devices-grid';
import { Notification } from '#components/common/notification';
import { NotificationType } from '#types/notification-type';

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
  @Output() onDelete = new EventEmitter<Owner>();

  protected notification: string | null = null;
  protected errorNotification: NotificationType = NotificationType.ERROR;

  constructor(private ownerService: OwnerService) {}

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.ownerService.deleteOwner(this.owner.id).subscribe({
      next: () => {
        this.onDelete.emit(this.owner);
      },
      error: () => {
        this.notification = 'An unexpected error occurred. Please try again.';
      },
    });
  }
}
