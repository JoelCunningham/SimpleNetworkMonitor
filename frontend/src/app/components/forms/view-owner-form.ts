import { ViewButtons } from '#components/buttons';
import { Notification } from '#components/common';
import { ViewField } from '#components/fields';
import { ViewDevicesGrid } from '#components/grids';
import { Owner } from '#interfaces';
import { OwnerService } from '#services';
import { NotificationType } from '#types';
import { Component, EventEmitter, Input, Output } from '@angular/core';

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
