import { BasicCard } from '#components/cards/basic-card';
import { Notification } from '#components/common/notification';
import { FormSection } from '#components/forms/form-section';
import { Select } from '#components/inputs/select';
import { Category } from '#interfaces/category';
import { Device } from '#interfaces/device';
import { Discovery } from '#interfaces/discovery';
import { Location } from '#interfaces/location';
import { Mac } from '#interfaces/mac';
import { Option, Value } from '#interfaces/option';
import { Owner } from '#interfaces/owner';
import { Port } from '#interfaces/port';
import { CategoryService } from '#services/category_service';
import { DeviceService } from '#services/device-service';
import { LocationService } from '#services/location-service';
import { OwnerService } from '#services/owner-service';
import { UtilitiesService } from '#services/utilities-service';
import { DeviceStatus } from '#types/device-status';
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
  selector: 'app-device-form',
  imports: [FormsModule, Select, Notification, BasicCard, FormSection],
  templateUrl: './device-form.html',
  styleUrl: './device-form.scss',
})
export class DeviceForm implements OnInit, OnChanges {
  @Input() device: Device | null = null;
  @Input() mode: FormMode | null = null;
  @Output() onClose = new EventEmitter<void>();
  @Output() onSubmit = new EventEmitter<Device>();
  @Output() onDelete = new EventEmitter<Device>();
  @Output() modeChange = new EventEmitter<FormMode>();

  protected macs: Mac[] = [];
  protected macOptions: Option[] = [];

  protected newModel: string = '';
  protected newMacs: Mac[] = [];

  private categories: Category[] = [];
  protected categoryOptions: Option[] = [];
  protected selectedCategory: Category | null = null;

  private locations: Location[] = [];
  protected locationOptions: Option[] = [];
  protected selectedLocation: Location | null = null;

  private owners: Owner[] = [];
  protected ownerOptions: Option[] = [];
  protected selectedOwner: Owner | null = null;

  protected genericError: boolean = false;
  protected modelError: boolean = false;
  protected categoryError: boolean = false;
  protected locationError: boolean = false;
  protected ownerError: boolean = false;
  protected macError: boolean = false;

  protected notificationType: NotificationType | null = null;
  protected notificationMessage: string | null = null;
  protected infoNotificationType: NotificationType = NotificationType.INFO;

  protected editMode: FormMode = FormMode.Edit;
  protected deviceName: string = 'Unknown Device';
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
    this.categoryService.currentCategories().subscribe((categories) => {
      this.categories = categories;
      this.categoryOptions = categories.map((category) => ({
        label: category.name,
        value: category.id,
      }));
    });

    this.locationService.currentLocations().subscribe((locations) => {
      this.locations = locations;
      this.locationOptions = locations.map((location) => ({
        label: location.name,
        value: location.id,
      }));
    });

    this.ownerService.currentOwners().subscribe((owners) => {
      this.owners = owners;
      this.ownerOptions = owners.map((owner) => ({
        label: owner.name,
        value: owner.id,
      }));
    });

    this.deviceService.currentDevices().subscribe((devices) => {
      this.macs = devices.flatMap((device) => device.macs || []);
      this.macOptions = this.macs.map((mac) => ({
        label: mac.address,
        value: mac.id,
      }));
    });

    this.initMode();
  }

  ngOnChanges() {
    if (!this.mode) {
      this.clearErrors();
    }
    if (this.device) {
      this.deviceName = this.utilitiesService.getDeviceName(this.device);
      this.deviceStatus = this.utilitiesService.getDeviceStatus(this.device);
      this.currentMac = this.device.primary_mac;
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
    if (this.device && (this.isEditMode() || this.isViewMode())) {
      this.newModel = this.device.model || '';
      this.selectedCategory = this.device.category || null;
      this.selectedLocation = this.device.location || null;
      this.selectedOwner = this.device.owner || null;
      this.newMacs = this.device.macs || [];
    }
    if (this.isAddMode()) {
    }
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
      console.log(this.notificationType, this.notificationMessage);
      return;
    }
    this.newMacs = this.newMacs.filter((m) => m.id !== mac.id);
  }

  getPortText(port: Port) {
    const portNumber = port.port || 'Unknown';
    const service = port.service ? ` (${port.service})` : '';
    return `${portNumber}${service}`;
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

  validateForm() {
    this.clearErrors();
    return true;
  }

  submitForm() {
    if (!this.validateForm()) return;

    const device: Device = {
      id: this.device && this.isEditMode() ? this.device.id : 0,
      model: this.device?.model || null,
      owner: this.device?.owner || null,
      category: this.device?.category || null,
      location: this.device?.location || null,
      primary_mac: this.device?.primary_mac || {
        id: 0,
        address: '',
        last_ip: '',
        last_seen: '',
      },
      macs: this.device?.macs || [],
    };

    const handleError = () => {
      this.genericError = true;
      this.setNotification('An unexpected error occurred. Please try again.');
      this.cdr.detectChanges();
    };

    if (this.isEditMode() && this.device) {
      this.deviceService.updateDevice(device).subscribe({
        next: (updatedDevice: Device) => {
          this.device = updatedDevice;
          this.setMode(FormMode.View);
          this.setNotification('Device updated successfully.');
          this.onSubmit.emit(updatedDevice);
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
      this.deviceService.createDevice(device).subscribe({
        next: (newDevice: Device) => {
          this.onSubmit.emit(newDevice);
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
        this.onDelete.emit(this.device!);
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
