import { Modal } from '#components/partials/modal';
import { Owner } from '#interfaces/owner';
import { OwnerService } from '#services/owner-service';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EditOwnerForm } from './owner-form/edit-owner-form';
import { ViewOwnerForm } from './owner-form/view-owner-form';

@Component({
  selector: 'app-owner-modal',
  imports: [Modal, ViewOwnerForm, EditOwnerForm],
  templateUrl: './owner-modal.html',
  styleUrl: './owner-modal.scss',
})
export class OwnerModal {
  @Input() owner!: Owner;
  @Input() isOpen: boolean = false;

  @Output() onClose = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  protected isViewMode: boolean = true;

  constructor(private ownerService: OwnerService) {}

  ngOnChanges() {
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

  getModalTitle(): string | null {
    if (this.isViewMode) {
      return 'View Owner';
    } else if (this.owner.id === 0) {
      return 'Add Owner';
    } else {
      return 'Edit Owner';
    }
  }

  setViewMode = (isViewMode: boolean) => (this.isViewMode = isViewMode);

  onFormClose() {
    if (this.owner.id !== 0 && !this.isViewMode) {
      this.setViewMode(true);
    } else {
      this.onClose.emit();
    }
  }

  onFormUpdate(owner: Owner) {
    this.owner = owner;
    this.setViewMode(true);
  }

  onFormDelete() {
    this.setViewMode(true);
    this.onDelete.emit();
  }
}
