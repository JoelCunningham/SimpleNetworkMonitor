import { EditDeviceButtons } from '#components/buttons';
import { BaseCard } from '#components/cards';
import { Checkbox, Icon, Notification, Select } from '#components/common';
import { EditField } from '#components/fields';
import {
  Category,
  Device,
  DeviceRequest,
  Location,
  Mac,
  Option,
  Owner,
} from '#interfaces';
import {
  CategoryService,
  DeviceService,
  LocationService,
  OwnerService,
  UtilitiesService,
} from '#services';
import { Constants, NotificationType } from '#types';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-edit-device-form',
  imports: [
    EditField,
    EditDeviceButtons,
    BaseCard,
    Select,
    Notification,
    Checkbox,
    Icon,
  ],
  templateUrl: './edit-device-form.html',
  styleUrl: './edit-device-form.scss',
})
export class EditDeviceForm {
  @Input() device!: Device;

  @Output() onSubmit = new EventEmitter<Device>();
  @Output() onCancel = new EventEmitter<void>();

  protected editDevice!: Device;
  protected isAutoNamed: boolean = true;

  protected categories: Option<Category>[] = [];
  protected locations: Option<Location>[] = [];
  protected owners: Option<Owner>[] = [];

  protected nameError: boolean = false;
  protected categoryError: boolean = false;

  protected notification: string | null = null;
  protected errorNotification: NotificationType = NotificationType.ERROR;

  constructor(
    private deviceService: DeviceService,
    private categoryService: CategoryService,
    private locationService: LocationService,
    private ownerService: OwnerService,
    private utilitiesService: UtilitiesService
  ) {}

  ngOnInit() {
    this.categoryService.currentCategories().subscribe((categories) => {
      this.categories = categories.map((category) => ({
        value: category,
        label: category.name,
        selected: this.editDevice.category?.id === category.id,
      }));
    });
    this.locationService.currentLocations().subscribe((locations) => {
      this.locations = locations.map((location) => ({
        value: location,
        label: location.name,
        selected: this.editDevice.location?.id === location.id,
      }));
    });

    this.ownerService.currentOwners().subscribe((owners) => {
      this.owners = owners.map((owner) => ({
        value: owner,
        label: owner.name,
        selected: this.editDevice.owner?.id === owner.id,
      }));
    });
  }

  ngOnChanges() {
    this.editDevice = { ...this.device };
    this.isAutoNamed = this.device.id ? !this.editDevice.name : true;
  }

  getAutoName(): string {
    if (!this.isAutoNamed && this.editDevice.name) {
      return this.editDevice.name;
    }
    return this.utilitiesService.getDisplayNameEx(
      this.owners.find((o) => o.selected)?.value?.name || '',
      this.locations.find((o) => o.selected)?.value?.name || '',
      this.categories.find((o) => o.selected)?.value?.name || ''
    );
  }

  removeMac(mac: Mac) {
    if (this.editDevice.macs.length === 1) {
      this.notification = 'At least one MAC address is required.';
      return;
    }
    this.editDevice.macs = this.editDevice.macs.filter((m) => m.id !== mac.id);
  }

  clearErrors() {
    this.nameError = false;
    this.categoryError = false;
    this.notification = null;
  }

  validateName() {
    if (this.isAutoNamed) return null;

    if (!this.editDevice.name || !this.editDevice.name.trim()) {
      return 'Device name is required when auto naming is disabled.';
    }
    const isReserved = Constants.RESERVED_NAMES.includes(
      this.editDevice.name.trim().toLowerCase()
    );
    if (isReserved) {
      return `Device name cannot be "${this.editDevice.name}".`;
    }
    return null;
  }

  validateCategory() {
    if (!this.categories.find((option) => option.selected)) {
      return 'Category is required.';
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

    const categoryValidationMessage = this.validateCategory();
    if (categoryValidationMessage) {
      this.categoryError = true;
      this.notification = categoryValidationMessage;
      return;
    }

    const request: DeviceRequest = {
      name: this.isAutoNamed ? null : this.editDevice.name,
      model: this.editDevice.model,
      owner_id: this.owners.find((o) => o.selected)?.value?.id ?? null,
      category_id: this.categories.find((o) => o.selected)?.value?.id ?? null,
      location_id: this.locations.find((o) => o.selected)?.value?.id ?? null,
      mac_ids: this.editDevice.macs.map((mac) => mac.id),
    };

    if (this.device.id) {
      this.deviceService.updateDevice(this.device.id, request).subscribe({
        next: (updatedDevice: Device) => {
          this.onSubmit.emit(updatedDevice);
          this.notification = 'Device updated successfully.';
        },
        error: () => {
          this.notification = Constants.GENERIC_ERROR_MESSAGE;
        },
      });
    } else {
      this.deviceService.createDevice(request).subscribe({
        next: (createdDevice: Device) => {
          this.onSubmit.emit(createdDevice);
        },
        error: () => {
          this.notification = Constants.GENERIC_ERROR_MESSAGE;
        },
      });
    }
  }

  cancel() {
    this.clearErrors();
    this.onCancel.emit();
  }
}
