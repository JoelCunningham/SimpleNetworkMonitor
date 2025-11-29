import { EditDeviceForm, ViewDeviceForm } from '#components/forms';
import { BaseModal } from '#components/modals';
import { Device, Notification } from '#interfaces';
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
  protected notification?: Notification;

  ngOnChanges() {
    this.notification = undefined;
  }

  getModalTitle() {
    if (this.isViewMode) {
      return 'View Device';
    } else if (this.device.id === 0) {
      return 'Add Device';
    } else {
      return 'Edit Device';
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

  onFormUpdate(device: Device) {
    this.device = device;
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
