import { BasePanel } from '#components/base/base-panel';
import { Icon } from '#components/common/icon';
import { DeviceService } from '#services/device-service';
import { ChangeDetectorRef, Component } from '@angular/core';

@Component({
  selector: 'app-status-panel',
  imports: [BasePanel, Icon],
  templateUrl: './status-panel.html',
  styleUrl: './status-panel.scss',
})
export class StatusPanel {
  protected isLiveView = true;
  protected lastScan: Date | null = null;

  constructor(
    private deviceService: DeviceService,
    private cdr: ChangeDetectorRef
  ) {
    this.deviceService.lastRefresh.subscribe((date) => {
      this.lastScan = date;
      this.cdr.detectChanges();
    });
  }

  lastScanFormatted() {
    return this.lastScan ? new Date(this.lastScan).toLocaleString() : 'Never';
  }

  toggleViewMode() {
    this.isLiveView = !this.isLiveView;
    this.deviceService.setAutoRefresh(this.isLiveView);
  }
}
