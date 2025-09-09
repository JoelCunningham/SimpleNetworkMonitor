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
  OnDestroy,
  OnInit,
  Output,
} from '@angular/core';
import { interval, Subscription } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-device-card',
  imports: [Icon],
  templateUrl: './device-card.html',
  styleUrl: './device-card.scss',
})
export class DeviceCard implements OnInit, OnDestroy {
  @Input() device: Device | null = null;
  @Input() owner: Owner | null = null;
  @Input() showLink: boolean = false;
  @Input() showStatus: boolean = false;
  @Input() showRemove: boolean = false;

  @Output() onClick = new EventEmitter<Owner | null>();
  @Output() cardRemoved = new EventEmitter<Device | null>();

  protected statusText: string = LastSeenStatus.NEVER;
  protected statusClass: string = DeviceStatus.OFFLINE;
  protected displayName: string = 'Unknown Device';
  protected portalUrl: string | null = null;

  private statusSubscription?: Subscription;

  constructor(
    private utilitiesService: UtilitiesService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit() {
    this.updateStatus();

    this.statusSubscription = interval(60000).subscribe(() => {
      this.updateStatus();
      this.cdr.detectChanges();
    });

    if (this.device) {
      this.displayName = this.utilitiesService.getDisplayName(this.device);
      this.portalUrl = this.utilitiesService.getDeviceHttpUrl(this.device);
    }
  }

  ngOnDestroy() {
    this.statusSubscription?.unsubscribe();
  }

  deviceIcon(): string {
    return this.device?.category?.name.toLowerCase() || 'unknown';
  }

  openInNewTab(): void {
    if (this.portalUrl) {
      window.open(this.portalUrl, '_blank');
    }
  }

  updateStatus() {
    if (!this.device) return;
    this.statusText = this.utilitiesService.getLastSeenStatus(this.device);
    this.statusClass = this.utilitiesService.getDeviceStatus(this.device);
  }

  handleClick() {
    this.onClick.emit(this.owner);
  }
}
