import { BasicCard } from '#components/cards/basic-card';
import { Icon } from '#components/common/icon';
import { Notification } from '#components/common/notification';
import { FormSection } from '#components/forms/form-section';
import { Checkbox } from '#components/inputs/checkbox';
import { Select } from '#components/inputs/select';
import { Device, DeviceRequest } from '#interfaces/device';
import { Discovery } from '#interfaces/discovery';
import { Mac } from '#interfaces/mac';
import { Option, Value } from '#interfaces/option';
import { Port } from '#interfaces/port';
import { CategoryService } from '#services/category_service';
import { DeviceService } from '#services/device-service';
import { LocationService } from '#services/location-service';
import { OwnerService } from '#services/owner-service';
import { UtilitiesService } from '#services/utilities-service';
import { DeviceStatus } from '#types/device-status';
import { FormMode } from '#types/form-mode';
import { NotificationType } from '#types/notification-type';
import { DatePipe } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  EventEmitter,
  Input,
  OnChanges,
  OnDestroy,
  OnInit,
  Output,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-device-form',
  imports: [
    DatePipe,
    FormsModule,
    Select,
    Notification,
    BasicCard,
    FormSection,
    Checkbox,
    Icon,
  ],
  templateUrl: './device-form.html',
  styleUrl: './device-form.scss',
})
export class DeviceForm implements OnInit, OnChanges, OnDestroy {
  @Input() device!: Device;
  @Input() mode!: FormMode;
  @Output() onClose = new EventEmitter<void>();
  @Output() modeChange = new EventEmitter<FormMode>();

  private subscriptions: Subscription = new Subscription();

  protected macs: Mac[] = [];
  protected macOptions: Option[] = [];

  protected categoryOptions: Option[] = [];
  protected selectedCategory?: Option;

  protected locationOptions: Option[] = [];
  protected selectedLocation?: Option;

  protected ownerOptions: Option[] = [];
  protected selectedOwner?: Option;

  protected newName: string | null = null;
  protected newModel: string = '';
  protected newMacs: Mac[] = [];
  protected autoName: boolean = true;

  protected genericError: boolean = false;
  protected nameError: boolean = false;
  protected modelError: boolean = false;
  protected categoryError: boolean = false;
  protected locationError: boolean = false;
  protected ownerError: boolean = false;
  protected macError: boolean = false;

  protected notificationType: NotificationType | null = null;
  protected notificationMessage: string | null = null;
  protected infoNotificationType: NotificationType = NotificationType.INFO;

  protected editMode: FormMode = FormMode.Edit;
  protected deviceStatus: DeviceStatus | null = null;

  protected currentMac: Mac | null = null;

  constructor(
    private deviceService: DeviceService,
    private categoryService: CategoryService,
    private locationService: LocationService,
    private ownerService: OwnerService,
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    if (!this.device) {
      throw new Error('DeviceForm: device is required');
    }
    if (!this.mode) {
      throw new Error('DeviceForm: mode is required');
    }

    this.subscriptions.add(
      this.categoryService.currentCategories().subscribe((categories) => {
        this.categoryOptions = categories.map((category) => ({
          label: category.name,
          value: category.id,
        }));
      })
    );

    this.subscriptions.add(
      this.locationService.currentLocations().subscribe((locations) => {
        this.locationOptions = locations.map((location) => ({
          label: location.name,
          value: location.id,
        }));
      })
    );

    this.subscriptions.add(
      this.ownerService.currentOwners().subscribe((owners) => {
        this.ownerOptions = owners.map((owner) => ({
          label: owner.name,
          value: owner.id,
        }));
      })
    );

    this.subscriptions.add(
      this.deviceService.currentDevices().subscribe((devices) => {
        this.macs = devices.flatMap((device) => device.macs || []);
        this.macOptions = this.macs.map((mac) => ({
          label: mac.address,
          value: mac.id,
        }));
      })
    );

    this.initMode();
  }

  ngOnChanges() {
    if (!this.mode) {
      this.clearErrors();
    }
    if (this.device) {
      this.currentMac = this.device.primary_mac;
      this.deviceStatus = this.utilitiesService.getDeviceStatus(this.device);
    }
    this.cdr.detectChanges();
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
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
    if (this.device && (this.isEditMode() || this.isViewMode())) {
      this.newName = this.device.name || null;
      this.newModel = this.device.model || '';
      this.autoName = !this.device.name;

      this.selectedCategory = this.getSelectedOption(
        this.device.category?.id,
        this.categoryOptions
      );
      this.selectedLocation = this.getSelectedOption(
        this.device.location?.id,
        this.locationOptions
      );
      this.selectedOwner = this.getSelectedOption(
        this.device.owner?.id,
        this.ownerOptions
      );
    }
    this.newMacs = this.device.macs || [];
  }

  getSelectedOption(id: number | undefined, options: Option[]) {
    const option = options.find((option) => option.value === id) || undefined;
    return option;
  }

  cancelEdit() {
    this.setMode(FormMode.View);
  }

  setNotification(message: string | null) {
    const hasError =
      this.genericError ||
      this.modelError ||
      this.categoryError ||
      this.macError ||
      this.locationError ||
      this.ownerError;

    this.notificationType = hasError
      ? NotificationType.ERROR
      : NotificationType.SUCCESS;
    this.notificationMessage = message;
  }

  clearErrors() {
    this.genericError = false;
    this.modelError = false;
    this.categoryError = false;
    this.macError = false;
    this.locationError = false;
    this.ownerError = false;
    this.setNotification(null);
  }

  selectMac(mac: Mac) {
    this.currentMac = mac;
  }

  removeMac(mac: Mac) {
    if (this.newMacs.length === 1) {
      this.macError = true;
      this.setNotification('At least one MAC address is required.');
      this.cdr.detectChanges();
      return;
    }
    this.newMacs = this.newMacs.filter((m) => m.id !== mac.id);
  }

  setCategory(categoryId: Value) {
    this.selectedCategory = this.categoryOptions.find(
      (category) => category.value === categoryId
    )!;
    this.clearErrors();
  }

  setLocation(locationId: Value) {
    this.selectedLocation = this.locationOptions.find(
      (location) => location.value === locationId
    )!;
    this.clearErrors();
  }

  setOwner(ownerId: Value) {
    this.selectedOwner = this.ownerOptions.find(
      (owner) => owner.value === ownerId
    )!;
    this.clearErrors();
  }

  toggleAutoName(checked: boolean) {
    this.autoName = checked;
  }

  getPortText(port: Port) {
    const portNumber = port.port || 'Unknown';
    const service = port.service ? ` (${port.service})` : '';
    return `${portNumber}${service}`;
  }

  getPortHttpUrl(ip: string | undefined, port: number): string | null {
    if (!ip) return null;
    return this.utilitiesService.getPortHttpUrl(ip, port);
  }

  getSortedPorts(mac: Mac | null): Port[] {
    if (!mac || !mac.ports) return [];
    return [...mac.ports].sort((a, b) => (a.port || 0) - (b.port || 0));
  }

  getDiscoveryText(discovery: Discovery) {
    const name = discovery.device_name || discovery.device_type || 'Unknown';
    let discoveryDetails = [];
    if (discovery.manufacturer) {
      discoveryDetails.push(`Mfg: ${discovery.manufacturer}`);
    }
    if (discovery.model) {
      discoveryDetails.push(`Model: ${discovery.model}`);
    }
    if (discovery.protocol) {
      discoveryDetails.push(`via ${discovery.protocol}`);
    }
    return discoveryDetails.length > 0
      ? `${name} (${discoveryDetails.join(', ')})`
      : name;
  }

  getAutoName(
    category: Option | null | undefined,
    location: Option | null | undefined,
    owner: Option | null | undefined
  ): string {
    const ownerName = owner ? owner.label : '';
    const locationName = location ? location.label : '';
    const categoryName = category ? category.label : '';
    return this.utilitiesService.getDisplayNameEx(
      ownerName,
      locationName,
      categoryName
    );
  }

  validateForm() {
    this.clearErrors();

    if (!this.selectedCategory) {
      this.categoryError = true;
      this.setNotification('Category is required.');
      return false;
    }

    return true;
  }

  submitForm() {
    if (!this.validateForm()) return;

    const request: DeviceRequest = {
      name: this.autoName ? null : this.newName,
      model: this.newModel,
      owner_id: this.selectedOwner?.value ?? null,
      category_id: this.selectedCategory?.value ?? null,
      location_id: this.selectedLocation?.value ?? null,
      mac_ids: this.newMacs.map((mac) => mac.id),
    };

    const handleError = (error: any) => {
      console.error('Device operation error:', error);
      this.genericError = true;
      this.setNotification('An unexpected error occurred. Please try again.');
      this.cdr.detectChanges();
    };

    if (this.isEditMode() && this.device) {
      this.deviceService.updateDevice(this.device.id, request).subscribe({
        next: (updatedDevice: Device) => {
          this.device = updatedDevice;
          this.setMode(FormMode.View);
          this.setNotification('Device updated successfully.');
          this.cdr.detectChanges();
        },
        error: handleError,
      });
    } else {
      this.deviceService.createDevice(request).subscribe({
        next: () => {
          this.closeForm();
        },
        error: handleError,
      });
    }
  }

  deleteDevice() {
    if (!this.device) return;
    this.deviceService.deleteDevice(this.device.id).subscribe({
      next: () => {
        this.setNotification('Device deleted successfully.');
        this.closeForm();
      },
      error: () => {
        this.setNotification('An error occurred while deleting the device.');
      },
    });
  }

  closeForm() {
    this.clearErrors();
    this.onClose.emit();
  }
}
