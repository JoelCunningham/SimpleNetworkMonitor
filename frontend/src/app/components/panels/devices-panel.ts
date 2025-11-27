import { DeviceCard } from '#components/cards';
import { Select } from '#components/common';
import { DeviceModal } from '#components/modals';
import { BasePanel } from '#components/panels';
import {
  Category,
  Device,
  Location,
  Mac,
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
  UtilitiesService,
} from '#services';
import { FormMode, NotificationType } from '#types';
import {
  ChangeDetectorRef,
  Component,
  Input,
  OnDestroy,
  OnInit,
} from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Subscription } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-devices-panel',
  imports: [BasePanel, DeviceCard, Select, FormsModule, DeviceModal],
  templateUrl: './devices-panel.html',
  styleUrl: './devices-panel.scss',
})
export class DevicesPanel implements OnInit, OnDestroy {
  @Input() showUnknown: boolean = false;

  private subscriptions: Subscription = new Subscription();

  private devices: Device[] = [];
  protected deviceList: Device[] = [];
  protected currentDevice: Device | null = null;

  protected ownerOptions: Option<Owner>[] = [];
  protected selectedOwner: Option<Owner> | null = null;

  protected locationOptions: Option<Location>[] = [];
  protected selectedLocation: Option<Location> | null = null;

  protected categoryOptions: Option<Category>[] = [];
  protected selectedCategory: Option<Category> | null = null;

  protected notification: Notification | null = null;

  protected showDeviceModal = false;
  protected deviceFormMode: FormMode | null = null;

  protected titleText = 'Devices';
  protected timeLimit: number = 7;

  constructor(
    private deviceService: DeviceService,
    private macService: MacService,
    private ownerService: OwnerService,
    private locationService: LocationService,
    private categoryService: CategoryService,
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    if (!this.showUnknown) {
      this.titleText = 'My Devices';
      this.subscriptions.add(
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
        })
      );
    } else {
      this.titleText = 'Unknown Devices';
      this.subscriptions.add(
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
        })
      );
    }

    this.subscriptions.add(
      this.ownerService.currentOwners().subscribe((owners) => {
        this.ownerOptions = owners
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((owner) => ({
            value: owner,
            label: owner.name,
          }));
        this.cdr.markForCheck();
      })
    );

    this.subscriptions.add(
      this.locationService.currentLocations().subscribe((locations) => {
        this.locationOptions = locations
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((location) => ({
            value: location,
            label: location.name,
          }));
        this.cdr.markForCheck();
      })
    );

    this.subscriptions.add(
      this.categoryService.currentCategories().subscribe((categories) => {
        this.categoryOptions = categories
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((category) => ({
            value: category,
            label: category.name,
          }));
        this.cdr.markForCheck();
      })
    );
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  protected applyFilters() {
    this.deviceList = this.devices.filter((device) => {
      const ownerMatch = this.selectedOwner
        ? device.owner?.id === this.selectedOwner.value?.id
        : true;
      const locationMatch = this.selectedLocation
        ? device.location?.id === this.selectedLocation.value?.id
        : true;
      const categoryMatch = this.selectedCategory
        ? device.category?.id === this.selectedCategory.value?.id
        : true;
      const timeMatch = this.showUnknown
        ? (() => {
            if (!this.timeLimit || this.timeLimit <= 0) return true;
            const cutoff = Date.now() - this.timeLimit * 24 * 60 * 60 * 1000;
            const latest = this.getLatestMacTime(device);
            return latest >= cutoff;
          })()
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
    this.selectedOwner = null;
    this.selectedLocation = null;
    this.selectedCategory = null;
    this.applyFilters();
  }

  getModalTitle(): string | null {
    switch (this.deviceFormMode) {
      case FormMode.Add:
        return 'Add Device';
      case FormMode.View:
        return this.utilitiesService.getDisplayName(this.currentDevice);
      case FormMode.Edit:
        return 'Edit Device';
      default:
        return null;
    }
  }

  openViewModal(device: Device) {
    this.openModal(device, FormMode.View);
  }

  openAddModal(device: Device) {
    this.openModal(device, FormMode.Add);
  }

  openModal(device: Device, form: FormMode) {
    this.currentDevice = device;
    this.deviceFormMode = form;
    this.showDeviceModal = true;
  }

  onAddedToDevice(device: Device) {
    this.currentDevice = device;
    this.deviceFormMode = FormMode.View;
    this.showDeviceModal = true;
  }

  closeModal() {
    this.showDeviceModal = false;
    setTimeout(() => {
      this.deviceFormMode = null;
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
