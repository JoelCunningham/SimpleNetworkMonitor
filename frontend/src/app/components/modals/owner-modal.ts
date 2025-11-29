import { EditOwnerForm, ViewOwnerForm } from '#components/forms';
import { BaseModal } from '#components/modals';
import { Notification, Owner } from '#interfaces';
import { OwnerService } from '#services';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-owner-modal',
  imports: [BaseModal, ViewOwnerForm, EditOwnerForm],
  templateUrl: './owner-modal.html',
  styleUrl: './owner-modal.scss',
})
export class OwnerModal {
  @Input() owner!: Owner;
  @Input() isOpen: boolean = false;

  @Output() onClose = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  protected isViewMode: boolean = true;
  protected notification?: Notification;

  constructor(private ownerService: OwnerService) {}

  ngOnChanges() {
    this.notification = undefined;
    this.isViewMode = this.owner.id !== 0;

    this.ownerService.currentOwners().subscribe((owners: Owner[]) => {
      if (this.owner.id && this.owner.id !== 0) {
        const updated = owners.find((o: Owner) => o.id === this.owner.id);
        if (updated) {
          this.owner = updated;
        }
      }
    });
  }

  getModalTitle() {
    if (this.isViewMode) {
      return 'View Owner';
    } else if (this.owner.id === 0) {
      return 'Add Owner';
    } else {
      return 'Edit Owner';
    }
  }

  setViewMode(isViewMode: boolean) {
    this.isViewMode = isViewMode;
  }

  onFormClose() {
    this.onClose.emit();
  }

  onFormCancel() {
    this.setViewMode(true);
  }

  onFormUpdate(owner: Owner) {
    this.owner = owner;
    this.setViewMode(true);
  }

  onFormDelete() {
    this.setViewMode(true);
    this.onDelete.emit();
  }

  onNotification(notification?: Notification) {
    this.notification = notification;
  }
}
