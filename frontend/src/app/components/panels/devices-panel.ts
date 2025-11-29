import { DeviceCard } from '#components/cards';
import { Select } from '#components/common';
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
  MacService,
  OwnerService,
} from '#services';
import { NotificationType } from '#types';
import { ChangeDetectorRef, Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  standalone: true,
  selector: 'app-devices-panel',
  imports: [BasePanel, DeviceCard, Select, FormsModule, DeviceModal],
  templateUrl: './devices-panel.html',
  styleUrl: './devices-panel.scss',
})
export class DevicesPanel {
  @Input() showUnknown: boolean = false;

  private devices: Device[] = [];
  protected deviceList: Device[] = [];
  protected currentDevice: Device | null = null;

  protected owners: Option<Owner>[] = [];
  protected locations: Option<Location>[] = [];
  protected categories: Option<Category>[] = [];

  protected notification: Notification | null = null;

  protected showDeviceModal = false;

  protected titleText = 'Devices';
  protected timeLimit: number = 7;

  constructor(
    private deviceService: DeviceService,
    private macService: MacService,
    private ownerService: OwnerService,
    private locationService: LocationService,
    private categoryService: CategoryService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    if (!this.showUnknown) {
      this.titleText = 'My Devices';
      this.deviceService.currentDevices().subscribe((devices) => {
        this.devices = devices;
        this.deviceList = this.sortDevices(devices);

        if (this.currentDevice) {
          this.currentDevice =
            this.devices.find(
              (device) => device.id === this.currentDevice!.id
            ) || null;
        }

        this.applyFilters();
        this.cdr.detectChanges();
      });
    } else {
      this.titleText = 'Unknown Devices';
      this.macService.currentMacs().subscribe((macs) => {
        this.devices = macs.map((mac) => {
          const deviceFromMac: Device = {
            id: 0,
            name: mac.address,
            model: null,
            category: null,
            location: null,
            owner: null,
            macs: [mac],
            primary_mac: mac,
          };
          return deviceFromMac;
        });

        this.deviceList = this.sortDevices(this.devices);

        if (this.currentDevice) {
          this.currentDevice =
            this.devices.find(
              (device) => device.id === this.currentDevice!.id
            ) || null;
        }

        this.applyFilters();
        this.cdr.detectChanges();
      });
    }

    this.ownerService.currentOwners().subscribe((owners) => {
      this.owners = owners
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((owner) => ({
          value: owner,
          label: owner.name,
        }));
      this.cdr.markForCheck();
    });

    this.locationService.currentLocations().subscribe((locations) => {
      this.locations = locations
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((location) => ({
          value: location,
          label: location.name,
        }));
      this.cdr.markForCheck();
    });

    this.categoryService.currentCategories().subscribe((categories) => {
      this.categories = categories
        .sort((a, b) => a.name.localeCompare(b.name))
        .map((category) => ({
          value: category,
          label: category.name,
        }));
      this.cdr.markForCheck();
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
      const timeMatch = this.showUnknown
        ? this.getLatestMacTime(device) >=
          Date.now() - this.timeLimit * 24 * 60 * 60 * 1000
        : true;
      return ownerMatch && locationMatch && categoryMatch && timeMatch;
    });

    if (this.deviceList.length === 0) {
      this.notification = {
        type: NotificationType.INFO,
        message: 'No devices found',
      };
    } else {
      this.notification = null;
    }
  }

  clearFilters() {
    this.owners.forEach((owner) => (owner.selected = false));
    this.locations.forEach((location) => (location.selected = false));
    this.categories.forEach((category) => (category.selected = false));
    this.applyFilters();
  }

  openModal(device: Device) {
    this.currentDevice = device;
    this.showDeviceModal = true;
  }

  closeModal() {
    this.showDeviceModal = false;
    setTimeout(() => {
      this.currentDevice = null;
      this.cdr.detectChanges();
    }, 100);
  }

  private sortDevices(devices: Device[]): Device[] {
    return devices.sort((a, b) => {
      const aLatestMac = this.getLatestMacTime(a);
      const bLatestMac = this.getLatestMacTime(b);
      if (bLatestMac !== aLatestMac) return bLatestMac - aLatestMac;
      return (a.macs[0]?.hostname || '').localeCompare(
        b.macs[0]?.hostname || ''
      );
    });
  }

  private getLatestMacTime(device: Device): number {
    return device.macs
      .map((mac) => (mac.last_seen ? new Date(mac.last_seen).getTime() : 0))
      .reduce((max, current) => Math.max(max, current), 0);
  }
}
