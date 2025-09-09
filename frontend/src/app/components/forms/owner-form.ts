import { DeviceCard } from '#components/cards/device-card';
import { Notification } from '#components/common/notification';
import { Select } from '#components/inputs/select';
import { Device } from '#interfaces/device';
import { Option, Value } from '#interfaces/option';
import { Owner } from '#interfaces/owner';
import { DeviceService } from '#services/device-service';
import { OwnerService } from '#services/owner-service';
import { UtilitiesService } from '#services/utilities-service';
import { FormMode } from '#types/form-mode';
import { NotificationType } from '#types/notification-type';
import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnInit,
  Output,
} from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-owner-form',
  imports: [FormsModule, Select, DeviceCard, Notification],
  templateUrl: './owner-form.html',
  styleUrl: './owner-form.scss',
})
export class OwnerForm implements OnInit, OnChanges {
  @Input() owner!: Owner;
  @Input() mode!: FormMode;
  @Output() onClose = new EventEmitter<void>();
  @Output() onSubmit = new EventEmitter<Owner>();
  @Output() onDelete = new EventEmitter<Owner>();
  @Output() modeChange = new EventEmitter<FormMode>();

  protected devices: Device[] = [];
  protected deviceOptions: Option[] = [];

  protected newName: string = '';
  protected newDevices: Device[] = [];

  protected editMode = FormMode.Edit;

  protected notificationType: NotificationType | null = null;
  protected notificationMessage: string | null = null;

  protected genericError: boolean = false;
  protected nameError: boolean = false;

  private RESERVED_NAMES = ['none', 'owner'];

  constructor(
    private cdr: ChangeDetectorRef,
    private ownerService: OwnerService,
    private deviceService: DeviceService,
    private utilitiesService: UtilitiesService
  ) {}

  ngOnInit() {
    if (!this.owner) {
      throw new Error('OwnerForm: owner is required');
    }
    if (!this.mode) {
      throw new Error('OwnerForm: mode is required');
    }

    this.deviceService.currentDevices().subscribe((devices) => {
      this.devices = devices;
      this.deviceOptions = this.devices
        .filter((device) => !device.owner || device.owner === null)
        .filter((device) => device.id)
        .map((device) => ({
          value: device.id,
          label: this.utilitiesService.getDisplayName(device),
        }));
      this.cdr.detectChanges();
    });

    this.initMode();
  }

  ngOnChanges() {
    if (!this.mode) {
      this.clearErrors();
    }
  }

  isViewMode(): boolean {
    return this.mode === FormMode.View;
  }
  isEditMode(): boolean {
    return this.mode === FormMode.Edit;
  }
  isAddMode(): boolean {
    return this.mode === FormMode.Add;
  }

  setMode(mode: FormMode) {
    this.mode = mode;
    this.initMode();
    this.clearErrors();
    this.modeChange.emit(mode);
  }

  initMode() {
    if (this.owner && (this.isEditMode() || this.isViewMode())) {
      this.newName = this.owner.name;
      this.newDevices = [...this.owner.devices];
    }
    if (this.isAddMode()) {
      this.newName = '';
      this.newDevices = [];
    }
  }

  addDevice(deviceId: Value) {
    const device = this.devices.find((d) => d.id === deviceId);
    if (device) {
      this.newDevices = [...this.newDevices, device];
      this.deviceOptions = this.deviceOptions.filter(
        (d) => d.value !== device.id
      );
    }
  }

  removeDevice(device: Device | null) {
    if (device) {
      this.deviceOptions = [
        ...this.deviceOptions,
        {
          value: device.id,
          label: this.utilitiesService.getDisplayName(device),
        },
      ];
      this.newDevices = this.newDevices.filter((d) => d !== device);
    }
  }

  cancelEdit() {
    this.newName = this.owner.name || '';
    this.newDevices = [...this.owner.devices];
    this.setMode(FormMode.View);
  }

  setNotification(message: string | null) {
    const hasError = this.genericError || this.nameError;

    this.notificationType = hasError
      ? NotificationType.ERROR
      : NotificationType.SUCCESS;
    this.notificationMessage = message;
  }

  clearErrors() {
    this.genericError = false;
    this.nameError = false;
    this.setNotification(null);
  }

  validateForm() {
    this.clearErrors();

    if (!this.newName || !this.newName.trim()) {
      this.nameError = true;
      this.setNotification('Owner name is required.');
      return false;
    }

    if (this.RESERVED_NAMES.includes(this.newName.toLowerCase())) {
      this.nameError = true;
      this.setNotification(`Owner name cannot be "${this.newName}".`);
      return false;
    }

    return true;
  }

  submitForm() {
    if (!this.validateForm()) return;

    const owner: Owner = {
      id: this.owner && this.isEditMode() ? this.owner.id : 0,
      name: this.newName,
      devices: this.newDevices,
    };

    const handleError = () => {
      this.genericError = true;
      this.setNotification('An unexpected error occurred. Please try again.');
      this.cdr.detectChanges();
    };

    if (this.isEditMode() && this.owner) {
      this.ownerService.updateOwner(owner).subscribe({
        next: (updatedOwner: Owner) => {
          this.owner = updatedOwner;
          this.setMode(FormMode.View);
          this.setNotification('Owner updated successfully.');
          this.onSubmit.emit(updatedOwner);
          this.cdr.detectChanges();
        },
        error: () => {
          this.genericError = true;
          this.setNotification(
            'An unexpected error occurred. Please try again.'
          );
          this.cdr.detectChanges();
        },
      });
    } else {
      this.ownerService.createOwner(owner).subscribe({
        next: (newOwner: Owner) => {
          this.onSubmit.emit(newOwner);
          this.closeForm();
        },
        error: handleError,
      });
    }
  }

  deleteOwner() {
    if (!this.owner) return;
    this.ownerService.deleteOwner(this.owner.id).subscribe({
      next: () => {
        this.setNotification('Owner deleted successfully.');
        this.onDelete.emit(this.owner!);
        this.closeForm();
      },
      error: () => {
        this.setNotification('An error occurred while deleting the owner.');
      },
    });
  }

  closeForm() {
    this.newName = '';
    this.newDevices = [];

    this.clearErrors();
    this.onClose.emit();
  }
}
