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

  protected categoryOptions: Option<Category>[] = [];
  protected selectedCategory?: Option<Category>;

  protected locationOptions: Option<Location>[] = [];
  protected selectedLocation?: Option<Location>;

  protected ownerOptions: Option<Owner>[] = [];
  protected selectedOwner?: Option<Owner>;

  protected isAutoNamed: boolean = true;

  protected nameError: boolean = false;
  protected categoryError: boolean = false;

  protected notification: string | null = null;
  protected errorNotification: NotificationType = NotificationType.ERROR;

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

    this.selectedCategory = this.categoryOptions.find(
      (option) => option.value?.id === this.editDevice.category?.id
    );
    this.selectedLocation = this.locationOptions.find(
      (option) => option.value?.id === this.editDevice.location?.id
    );
    this.selectedOwner = this.ownerOptions.find(
      (option) => option.value?.id === this.editDevice.owner?.id
    );
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
