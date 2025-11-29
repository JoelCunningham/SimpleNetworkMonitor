import { ViewOwnerButtons } from '#components/buttons';
import { ViewField } from '#components/fields';
import { ViewDevicesGrid } from '#components/grids';
import { Notification, Owner } from '#interfaces';
import { OwnerService } from '#services';
import { Constants, NotificationType } from '#types';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-view-owner-form',
  imports: [ViewField, ViewDevicesGrid, ViewOwnerButtons],
  templateUrl: './view-owner-form.html',
  styleUrl: './view-owner-form.scss',
})
export class ViewOwnerForm {
  @Input() owner!: Owner;

  @Output() onEdit = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();
  @Output() onNotification = new EventEmitter<Notification>();

  constructor(private ownerService: OwnerService) {}

  edit() {
    this.onEdit.emit();
  }

  delete() {
    this.ownerService.deleteOwner(this.owner.id).subscribe({
      next: () => {
        this.onDelete.emit();
        this.onNotification.emit({
          type: NotificationType.SUCCESS,
          message: 'Owner deleted successfully.',
        });
      },
      error: () => {
        this.onNotification.emit({
          type: NotificationType.ERROR,
          message: Constants.GENERIC_ERROR_MESSAGE,
        });
      },
    });
  }
}
