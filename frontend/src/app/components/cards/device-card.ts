import { BaseCard } from '#components/base/base-card';
import { Icon } from '#components/common/icon';
import { Device } from '#interfaces/device';
import { Owner } from '#interfaces/owner';
import { UtilitiesService } from '#services/utilities-service';
import { DeviceStatus } from '#types/device-status';
import { LastSeenStatus } from '#types/last-seen-status';
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
import { interval, Subscription } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-device-card',
  imports: [BaseCard, Icon],
  templateUrl: './device-card.html',
  styleUrl: './device-card.scss',
})
export class DeviceCard implements OnInit, OnChanges, OnDestroy {
  @Input() device!: Device;
  @Input() owner: Owner | null = null;

  @Input() showLink: boolean = false;
  @Input() showStatus: boolean = false;

  @Input() removable: boolean = false;
  @Input() interactive: boolean = true;

  @Output() onClick = new EventEmitter<void>();
  @Output() onRemove = new EventEmitter<Device>();

  protected statusText: string = LastSeenStatus.NEVER;
  protected statusClass: string = DeviceStatus.OFFLINE;
  protected displayName: string = 'Unknown Device';
  protected portalUrl: string | null = null;
  protected iconName: string = 'unknown';

  private statusSubscription?: Subscription;

  constructor(
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.updateDeviceData();
    this.updateStatus();

    this.statusSubscription = interval(60000).subscribe(() => {
      this.updateStatus();
      this.cdr.detectChanges();
    });
  }

  ngOnChanges() {
    this.updateDeviceData();
    this.updateStatus();
    this.cdr.detectChanges();
  }

  ngOnDestroy() {
    this.statusSubscription?.unsubscribe();
  }

  openInNewTab(): void {
    if (this.portalUrl) {
      window.open(this.portalUrl, '_blank');
    }
  }

  private updateDeviceData() {
    if (this.device) {
      this.displayName = this.utilitiesService.getDisplayName(this.device);
      this.portalUrl = this.utilitiesService.getDeviceHttpUrl(this.device);
      this.iconName = this.device?.category?.name.toLowerCase() || 'unknown';
    }
  }

  private updateStatus() {
    if (!this.device) return;
    this.statusText = this.utilitiesService.getLastSeenStatus(this.device);
    this.statusClass = this.utilitiesService.getDeviceStatus(this.device);
  }

  click() {
    this.onClick.emit();
  }

  remove() {
    this.onRemove.emit(this.device);
  }
}
