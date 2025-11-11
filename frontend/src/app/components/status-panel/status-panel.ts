import { BasePanel } from '#components/base/base-panel';
import { LiveViewButton } from '#components/status-panel/live-view-button';
import { DeviceService } from '#services/device-service';
import { ChangeDetectorRef, Component } from '@angular/core';
import { LastScanText } from './last-scan-text';

@Component({
  selector: 'app-status-panel',
  imports: [BasePanel, LastScanText, LiveViewButton],
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

  toggleViewMode(isLiveView: boolean) {
    this.deviceService.setAutoRefresh(isLiveView);
  }
}
