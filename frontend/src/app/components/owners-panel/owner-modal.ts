import { Modal } from '#components/partials/modal';
import { Owner } from '#interfaces/owner';
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
  @Output() onUpdate = new EventEmitter<Owner>();
  @Output() onDelete = new EventEmitter<Owner>();

  protected isViewMode: boolean = true;

  ngOnChanges() {
    this.isViewMode = this.owner.id !== 0;
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
    this.onUpdate.emit(owner);
  }

  onFormDelete(owner: Owner) {
    this.setViewMode(true);
    this.onDelete.emit(owner);
  }
}
