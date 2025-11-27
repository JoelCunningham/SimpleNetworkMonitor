import { EditDeviceForm, ViewDeviceForm } from '#components/forms';
import { BaseModal } from '#components/modals';
import { Device } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-device-modal',
  imports: [BaseModal, ViewDeviceForm, EditDeviceForm],
  templateUrl: './device-modal.html',
  styleUrl: './device-modal.scss',
})
export class DeviceModal {
  @Input() device!: Device;
  @Input() isOpen: boolean = false;

  @Output() onClose = new EventEmitter<void>();
  @Output() onDelete = new EventEmitter<void>();

  protected isViewMode: boolean = true;

  ngOnChanges() {}

  getModalTitle(): string | null {
    if (this.isViewMode) {
      return 'View Device';
    } else if (this.device.id === 0) {
      return 'Add Device';
    } else {
      return 'Edit Device';
    }
  }

  setViewMode = (isViewMode: boolean) => (this.isViewMode = isViewMode);

  onFormClose() {
    if (this.device.id !== 0 && !this.isViewMode) {
      this.setViewMode(true);
    } else {
      this.onClose.emit();
    }
  }

  onFormUpdate(device: Device) {
    this.device = device;
    this.setViewMode(true);
  }

  onFormDelete() {
    this.setViewMode(true);
    this.onDelete.emit();
  }
}
