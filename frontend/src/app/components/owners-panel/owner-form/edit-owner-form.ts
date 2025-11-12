import { EditField } from '#components/common/edit-field';
import { Device } from '#interfaces/device';
import { Option, Value } from '#interfaces/option';
import { Owner } from '#interfaces/owner';
import { DeviceService } from '#services/device-service';
import { OwnerService } from '#services/owner-service';
import { UtilitiesService } from '#services/utilities-service';
import { GENERIC_ERROR_MESSAGE } from '#types/constants';
import { NotificationType } from '#types/notification-type';
import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';
import { EditButtons } from './edit-buttons';
import { EditDevicesGrid } from './edit-devices-grid';
import { Notification } from '#components/common/notification';

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

  selectDevice(deviceId: Value) {
    const device = this.allDevices.find((d) => d.id === deviceId);
    if (device) {
      this.owner.devices = [...this.owner.devices, device];
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
    this.owner.devices = this.owner.devices.filter((d) => d !== device);
  }

  clearErrors() {
    this.nameError = false;
    this.notification = null;
  }

  validateName() {
    if (!this.owner.name || !this.owner.name.trim()) {
      return 'Owner name is required.';
    }
    if (this.RESERVED_NAMES.includes(this.owner.name.trim().toLowerCase())) {
      return `Owner name cannot be "${this.owner.name}".`;
    }
    const isTaken = this.allOwners.some(
      (o) => o.name === this.owner.name && o.id !== this.owner.id
    );
    if (isTaken) {
      return `An owner with the name "${this.owner.name}" already exists.`;
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

    if (this.owner.id === 0) {
      this.ownerService.createOwner(this.owner).subscribe({
        next: (owner: Owner) => {
          this.onSubmit.emit(owner);
        },
        error: () => {
          this.notification = GENERIC_ERROR_MESSAGE;
          this.cdr.detectChanges();
        },
      });
    } else {
      this.ownerService.updateOwner(this.owner).subscribe({
        next: (owner: Owner) => {
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
