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
import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';

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

  protected allDevices: Device[] = [];
  protected unassignedDevices: Option<Device>[] = [];

  protected allMacs: Mac[] = [];
  protected macOptions: Option<Mac>[] = [];
  protected selectedMacs: Option<Mac>[] = [];

  protected categoryOptions: Option<Category>[] = [];
  protected selectedCategory?: Option<Category>;

  protected locationOptions: Option<Location>[] = [];
  protected selectedLocation?: Option<Location>;

  protected ownerOptions: Option<Owner>[] = [];
  protected selectedOwner?: Option<Owner>;

  protected isAutoNamed: boolean = true;

  protected notification: string | null = null;
  protected errorNotification: NotificationType = NotificationType.ERROR;

  protected nameError: boolean = false;
  protected categoryError: boolean = false;

  constructor(
    private deviceService: DeviceService,
    private categoryService: CategoryService,
    private locationService: LocationService,
    private ownerService: OwnerService,
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.categoryService.currentCategories().subscribe((categories) => {
      this.categoryOptions = categories.map((category) => ({
        value: category,
        label: category.name,
      }));
    });
    this.locationService.currentLocations().subscribe((locations) => {
      this.locationOptions = locations.map((location) => ({
        value: location,
        label: location.name,
      }));
    });

    this.ownerService.currentOwners().subscribe((owners) => {
      this.ownerOptions = owners.map((owner) => ({
        value: owner,
        label: owner.name,
      }));
    });
    this.deviceService.currentDevices().subscribe((devices) => {
      this.allDevices = devices.filter((device) => device.id);
      this.unassignedDevices = devices
        .sort((a, b) =>
          this.utilitiesService
            .getDisplayName(a)
            .localeCompare(this.utilitiesService.getDisplayName(b))
        )
        .map((device) => ({
          value: device,
          label: this.utilitiesService.getDisplayName(device),
        }));
      this.allMacs = devices.flatMap((device) => device.macs || []);
    });
  }

  ngOnChanges() {
    this.editDevice = { ...this.device };

    this.selectedCategory = this.categoryOptions.find(
      (option) => option.value === this.editDevice.category?.id
    );
    this.selectedLocation = this.locationOptions.find(
      (option) => option.value === this.editDevice.location?.id
    );
    this.selectedOwner = this.ownerOptions.find(
      (option) => option.value === this.editDevice.owner?.id
    );

    this.isAutoNamed = !this.editDevice.name;
  }

  ///////////////////////

  getAutoName(): string {
    if (!this.isAutoNamed && this.editDevice.name) {
      return this.editDevice.name;
    }
    return this.utilitiesService.getDisplayNameEx(
      this.editDevice.owner?.name || '',
      this.editDevice.location?.name || '',
      this.editDevice.category?.name || ''
    );
  }

  removeMac(mac: Mac) {
    if (this.editDevice.macs.length === 1) {
      this.notification = 'At least one MAC address is required.';
      this.cdr.detectChanges();
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
    if (!this.selectedCategory) {
      return 'Category is required.';
    }

    return null;
  }

  submitAddToDevice(device: Device) {
    const request: DeviceRequest = {
      name: device.name,
      model: device.model,
      owner_id: device.owner?.id ?? null,
      category_id: device.category?.id ?? null,
      location_id: device.location?.id ?? null,
      mac_ids: device.macs.map((mac) => mac.id),
    };

    this.deviceService.updateDevice(device.id, request).subscribe({
      next: (updatedDevice: Device) => {
        this.onSubmit.emit(updatedDevice);
      },
      error: () => {
        this.notification = Constants.GENERIC_ERROR_MESSAGE;
      },
    });
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
      owner_id: this.selectedOwner?.value?.id ?? null,
      category_id: this.selectedCategory?.value?.id ?? null,
      location_id: this.selectedLocation?.value?.id ?? null,
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
