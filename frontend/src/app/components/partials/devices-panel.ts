import { DeviceCard } from '#components/cards/device-card';
import { Notification } from '#components/common/notification';
import { DeviceForm } from '#components/forms/device-form';
import { Select } from '#components/inputs/select';
import { Modal } from '#components/partials//modal';
import { Category } from '#interfaces/category';
import { Device } from '#interfaces/device';
import { Location } from '#interfaces/location';
import { Option, Value } from '#interfaces/option';
import { Owner } from '#interfaces/owner';
import { CategoryService } from '#services/category_service';
import { DeviceService } from '#services/device-service';
import { LocationService } from '#services/location-service';
import { OwnerService } from '#services/owner-service';
import { UtilitiesService } from '#services/utilities-service';
import { FormMode } from '#types/form-mode';
import { NotificationType } from '#types/notification-type';

import { ChangeDetectorRef, Component, OnDestroy, OnInit } from '@angular/core';
import { Subscription } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-devices-panel',
  imports: [DeviceCard, Select, Notification, Modal, DeviceForm],
  templateUrl: './devices-panel.html',
  styleUrl: './devices-panel.scss',
})
export class DevicesPanel implements OnInit, OnDestroy {
  private subscriptions: Subscription = new Subscription();

  private devices: Device[] = [];
  protected deviceList: Device[] = [];
  protected currentDevice: Device | null = null;

  private owners: Owner[] = [];
  protected ownerOptions: Option[] = [];
  protected selectedOwner: Owner | undefined;

  private locations: Location[] = [];
  protected locationOptions: Option[] = [];
  protected selectedLocation: Location | undefined;

  private categories: Category[] = [];
  protected categoryOptions: Option[] = [];
  protected selectedCategory: Category | undefined;

  protected notificationType: NotificationType | null = null;
  protected notificationMessage: string | null = null;

  protected showDeviceModal = false;
  protected deviceFormMode: FormMode | null = null;

  constructor(
    private deviceService: DeviceService,
    private ownerService: OwnerService,
    private locationService: LocationService,
    private categoryService: CategoryService,
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
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

    this.subscriptions.add(
      this.ownerService.currentOwners().subscribe((owners) => {
        this.owners = owners;
        this.ownerOptions = owners
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((owner) => ({
            value: owner.id,
            label: owner.name,
          }));
        this.cdr.markForCheck();
      })
    );

    this.subscriptions.add(
      this.locationService.currentLocations().subscribe((locations) => {
        this.locations = locations;
        this.locationOptions = locations
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((location) => ({
            value: location.id,
            label: location.name,
          }));
        this.cdr.markForCheck();
      })
    );

    this.subscriptions.add(
      this.categoryService.currentCategories().subscribe((categories) => {
        this.categories = categories;
        this.categoryOptions = categories
          .sort((a, b) => a.name.localeCompare(b.name))
          .map((category) => ({
            value: category.id,
            label: category.name,
          }));
        this.cdr.markForCheck();
      })
    );
  }

  ngOnDestroy() {
    this.subscriptions.unsubscribe();
  }

  selectOwner(ownerId: Value) {
    this.selectedOwner = this.owners.find((o) => o.id === ownerId);
    this.applyFilters();
  }

  selectLocation(locationId: Value) {
    this.selectedLocation = this.locations.find((l) => l.id === locationId);
    this.applyFilters();
  }

  selectCategory(categoryId: Value) {
    this.selectedCategory = this.categories.find((c) => c.id === categoryId);
    this.applyFilters();
  }

  private applyFilters() {
    this.deviceList = this.devices.filter((device) => {
      const ownerMatch = this.selectedOwner
        ? device.owner?.id === this.selectedOwner.id
        : true;
      const locationMatch = this.selectedLocation
        ? device.location?.id === this.selectedLocation.id
        : true;
      const categoryMatch = this.selectedCategory
        ? device.category?.id === this.selectedCategory.id
        : true;
      return ownerMatch && locationMatch && categoryMatch;
    });

    if (this.deviceList.length === 0) {
      this.notificationType = NotificationType.INFO;
      this.notificationMessage = 'No devices found';
    } else {
      this.notificationType = null;
    }
  }

  clearFilters() {
    this.selectedOwner = undefined;
    this.selectedLocation = undefined;
    this.selectedCategory = undefined;
    this.ownerOptions = [...this.ownerOptions];
    this.locationOptions = [...this.locationOptions];
    this.categoryOptions = [...this.categoryOptions];
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
