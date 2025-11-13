import { EditButtons } from '#components/buttons';
import { Notification } from '#components/common';
import { EditField } from '#components/fields';
import { EditDevicesGrid } from '#components/grids';
import { Device, Option, Owner, OwnerRequest, Value } from '#interfaces';
import { DeviceService, OwnerService, UtilitiesService } from '#services';
import { GENERIC_ERROR_MESSAGE, NotificationType } from '#types';
import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-edit-owner-form',
  imports: [EditField, EditDevicesGrid, EditButtons, Notification],
  templateUrl: './edit-owner-form.html',
  styleUrl: './edit-owner-form.scss',
})
export class EditOwnerForm {
  @Input() owner!: Owner;

  @Output() onSubmit = new EventEmitter<Owner>();
  @Output() onCancel = new EventEmitter<void>();

  protected editOwner!: Owner;

  protected allOwners: Owner[] = [];
  protected allDevices: Device[] = [];
  protected unassignedDevices: Option[] = [];

  protected notification: string | null = null;
  protected errorNotification: NotificationType = NotificationType.ERROR;

  protected nameError: boolean = false;
  private RESERVED_NAMES = ['none', 'owner'];

  constructor(
    private ownerService: OwnerService,
    private deviceService: DeviceService,
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
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
          value: device.id,
          label: this.utilitiesService.getDisplayName(device),
        }));
    });
  }

  ngOnChanges() {
    this.editOwner = { ...this.owner };
  }

  selectDevice(deviceId: Value) {
    const device = this.allDevices.find((d) => d.id === deviceId);
    if (device) {
      this.editOwner.devices = [...(this.editOwner.devices || []), device];
      this.unassignedDevices = this.unassignedDevices.filter(
        (d) => d.value !== device.id
      );
    }
  }

  removeDevice(device: Device) {
    this.unassignedDevices = [
      ...this.unassignedDevices,
      {
        value: device.id,
        label: this.utilitiesService.getDisplayName(device),
      },
    ];
    this.editOwner.devices = (this.editOwner.devices || []).filter(
      (d) => d !== device
    );
  }

  clearErrors() {
    this.nameError = false;
    this.notification = null;
  }

  validateName() {
    if (!this.editOwner.name || !this.editOwner.name.trim()) {
      return 'Owner name is required.';
    }
    if (
      this.RESERVED_NAMES.includes(this.editOwner.name.trim().toLowerCase())
    ) {
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
      this.notification = nameValidationMessage;
      return;
    }

    const ownerRequest: OwnerRequest = {
      name: this.editOwner.name,
      device_ids: this.editOwner.devices.map((device) => device.id),
    };

    if (this.editOwner.id === 0) {
      this.ownerService.createOwner(ownerRequest).subscribe({
        next: (owner) => {
          // emit full owner so UI can replace temp object immediately
          this.onSubmit.emit(owner);
        },
        error: () => {
          this.notification = GENERIC_ERROR_MESSAGE;
          this.cdr.detectChanges();
        },
      });
    } else {
      this.ownerService.updateOwner(this.owner.id, ownerRequest).subscribe({
        next: (owner) => {
          // emit full owner so UI can update immediately
          this.onSubmit.emit(owner);
        },
        error: () => {
          this.notification = GENERIC_ERROR_MESSAGE;
          this.cdr.detectChanges();
        },
      });
    }
  }

  cancel() {
    this.onCancel.emit();
  }
}
