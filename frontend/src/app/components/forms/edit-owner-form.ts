import { EditOwnerButtons } from '#components/buttons';
import { EditField } from '#components/fields';
import { EditDevicesGrid } from '#components/grids';
import { Device, Notification, Option, Owner, OwnerRequest } from '#interfaces';
import { DeviceService, OwnerService, UtilitiesService } from '#services';
import { Constants, NotificationType } from '#types';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-edit-owner-form',
  imports: [EditField, EditDevicesGrid, EditOwnerButtons],
  templateUrl: './edit-owner-form.html',
  styleUrl: './edit-owner-form.scss',
})
export class EditOwnerForm {
  @Input() owner!: Owner;

  @Output() onSubmit = new EventEmitter<Owner>();
  @Output() onCancel = new EventEmitter<void>();
  @Output() onNotification = new EventEmitter<Notification>();

  protected editOwner!: Owner;

  protected allOwners: Owner[] = [];
  protected allDevices: Device[] = [];
  protected unassignedDevices: Option<Device>[] = [];

  protected nameError: boolean = false;

  constructor(
    private ownerService: OwnerService,
    private deviceService: DeviceService,
    private utilitiesService: UtilitiesService
  ) {}

  ngOnInit() {
    this.ownerService.currentOwners().subscribe((owners) => {
      this.allOwners = owners;
    });
    this.deviceService.currentDevices().subscribe((devices) => {
      this.allDevices = devices;
      this.unassignedDevices = devices
        .filter((device) => !device.owner || device.owner === null)
        .filter((device) => device.id)
        .sort((a, b) =>
          this.utilitiesService
            .getDisplayName(a)
            .localeCompare(this.utilitiesService.getDisplayName(b))
        )
        .map((device) => ({
          value: device,
          label: this.utilitiesService.getDisplayName(device),
        }));
    });
  }

  ngOnChanges() {
    this.editOwner = { ...this.owner };
  }

  selectDevice(device: Device) {
    if (device) {
      this.editOwner.devices = [...(this.editOwner.devices || []), device];
      this.unassignedDevices = this.unassignedDevices.filter(
        (d) => d.value?.id !== device.id
      );
    }
  }

  removeDevice(device: Device) {
    this.unassignedDevices = [
      ...this.unassignedDevices,
      {
        value: device,
        label: this.utilitiesService.getDisplayName(device),
      },
    ];
    this.editOwner.devices = (this.editOwner.devices || []).filter(
      (d) => d !== device
    );
  }

  clearErrors() {
    this.nameError = false;
  }

  validateName() {
    if (!this.editOwner.name || !this.editOwner.name.trim()) {
      return 'Owner name is required.';
    }
    const isReserved = Constants.RESERVED_NAMES.includes(
      this.editOwner.name.trim().toLowerCase()
    );
    if (isReserved) {
      return `Owner name cannot be "${this.editOwner.name}".`;
    }
    const isTaken = this.allOwners.some(
      (o) => o.name === this.editOwner.name && o.id !== this.editOwner.id
    );
    if (isTaken) {
      return `An owner with the name "${this.editOwner.name}" already exists.`;
    }
    return null;
  }

  submit() {
    this.clearErrors();

    const nameValidationMessage = this.validateName();
    if (nameValidationMessage) {
      this.nameError = true;
      this.onNotification.emit({
        type: NotificationType.ERROR,
        message: nameValidationMessage,
      });
      return;
    }

    const ownerRequest: OwnerRequest = {
      name: this.editOwner.name,
      device_ids: this.editOwner.devices.map((device) => device.id),
    };

    if (this.editOwner.id === 0) {
      this.ownerService.createOwner(ownerRequest).subscribe({
        next: (owner) => {
          this.onSubmit.emit(owner);
          this.onNotification.emit({
            type: NotificationType.SUCCESS,
            message: `Owner created successfully.`,
          });
        },
        error: () => {
          this.onNotification.emit({
            type: NotificationType.ERROR,
            message: Constants.GENERIC_ERROR_MESSAGE,
          });
        },
      });
    } else {
      this.ownerService.updateOwner(this.owner.id, ownerRequest).subscribe({
        next: (owner) => {
          this.onSubmit.emit(owner);
          this.onNotification.emit({
            type: NotificationType.SUCCESS,
            message: `Owner updated successfully.`,
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

  cancel() {
    this.onCancel.emit();
  }
}
