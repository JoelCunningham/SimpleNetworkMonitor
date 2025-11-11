import { BasePanel } from '#components/base/base-panel';
import { LiveViewButton } from '#components/status-panel/live-view-button';
import { DeviceService } from '#services/device-service';
import { ChangeDetectorRef, Component } from '@angular/core';

@Component({
  selector: 'app-status-panel',
  imports: [BasePanel, LiveViewButton],
  templateUrl: './status-panel.html',
  styleUrl: './status-panel.scss',
})
export class StatusPanel {
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

  toggleViewMode(isLiveView: boolean) {
    this.deviceService.setAutoRefresh(isLiveView);
  }
}
