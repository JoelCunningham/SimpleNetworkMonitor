import { FilterUnknownDeviceButtons } from '#components/buttons';
import { DeviceCard } from '#components/cards';
import { DeviceModal } from '#components/modals';
import { BasePanel } from '#components/panels';
import { Device, Notification } from '#interfaces';
import { MacService, UtilitiesService } from '#services';
import { NotificationType } from '#types';
import { ChangeDetectorRef, Component } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-unknown-devices-panel',
  imports: [BasePanel, DeviceCard, DeviceModal, FilterUnknownDeviceButtons],
  templateUrl: './unknown-devices-panel.html',
  styleUrl: './unknown-devices-panel.scss',
})
export class UnknownDevicesPanel {
  private devices: Device[] = [];
  protected deviceList: Device[] = [];
  protected currentDevice?: Device;

  protected timeLimit: number = 7;

  protected notification?: Notification;
  protected showDeviceModal = false;

  constructor(
    private macService: MacService,
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
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

      this.deviceList = this.utilitiesService.sortDevices(this.devices);

      this.applyFilters();
    });
  }

  applyFilters() {
    this.deviceList = this.devices.filter(
      (device) =>
        this.utilitiesService.getLatestMacTime(device) >=
        Date.now() - this.timeLimit * 24 * 60 * 60 * 1000
    );

    if (this.deviceList.length === 0) {
      this.notification = {
        type: NotificationType.INFO,
        message: 'All clear!',
      };
    } else {
      this.notification = undefined;
    }

    this.cdr.detectChanges();
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
