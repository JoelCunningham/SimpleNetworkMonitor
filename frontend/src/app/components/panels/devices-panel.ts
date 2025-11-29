import { FilterDeviceButtons } from '#components/buttons';
import { DeviceCard } from '#components/cards';
import { DeviceModal } from '#components/modals';
import { BasePanel } from '#components/panels';
import {
  Category,
  Device,
  Location,
  Notification,
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
import { NotificationType } from '#types';
import { Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-devices-panel',
  imports: [BasePanel, DeviceCard, DeviceModal, FilterDeviceButtons],
  templateUrl: './devices-panel.html',
  styleUrl: './devices-panel.scss',
})
export class DevicesPanel {
  private devices: Device[] = [];
  protected deviceList: Device[] = [];
  protected currentDevice?: Device;

  protected owners: Option<Owner>[] = [];
  protected locations: Option<Location>[] = [];
  protected categories: Option<Category>[] = [];

  protected notification?: Notification;
  protected showDeviceModal = false;

  constructor(
    private deviceService: DeviceService,
    private ownerService: OwnerService,
    private locationService: LocationService,
    private categoryService: CategoryService,
    private utilitiesService: UtilitiesService
  ) {}

  ngOnInit() {
    this.deviceService.currentDevices().subscribe((devices) => {
      this.devices = devices;
      this.deviceList = this.utilitiesService.sortDevices(devices);
      this.applyFilters();
    });

    this.ownerService.currentOwners().subscribe((owners) => {
      this.owners = owners
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((owner) => ({
          value: owner,
          label: owner.name,
        }));
    });

    this.locationService.currentLocations().subscribe((locations) => {
      this.locations = locations
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((location) => ({
          value: location,
          label: location.name,
        }));
    });

    this.categoryService.currentCategories().subscribe((categories) => {
      this.categories = categories
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((category) => ({
          value: category,
          label: category.name,
        }));
    });
  }

  selectedOwner = () =>
    this.owners.find((owner) => owner.selected)?.value || null;
  selectedLocation = () =>
    this.locations.find((location) => location.selected)?.value || null;
  selectedCategory = () =>
    this.categories.find((category) => category.selected)?.value || null;

  applyFilters() {
    this.deviceList = this.devices.filter((device) => {
      const ownerMatch = this.selectedOwner()
        ? device.owner?.id === this.selectedOwner()?.id
        : true;
      const locationMatch = this.selectedLocation()
        ? device.location?.id === this.selectedLocation()?.id
        : true;
      const categoryMatch = this.selectedCategory()
        ? device.category?.id === this.selectedCategory()?.id
        : true;
      return ownerMatch && locationMatch && categoryMatch;
    });

    if (this.deviceList.length === 0) {
      this.notification = {
        type: NotificationType.INFO,
        message: 'No devices found',
      };
    } else {
      this.notification = undefined;
    }
  }

  openModal(device: Device) {
    this.currentDevice = device;
    this.showDeviceModal = true;
  }

  closeModal() {
    this.showDeviceModal = false;
    setTimeout(() => {
      this.currentDevice = undefined;
    }, 100);
  }
}
