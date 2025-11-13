import { LiveViewButton } from '#components/buttons/live-view-button';
import { LastScanText } from '#components/fields/last-scan-text';
import { BasePanel } from '#components/panels/base-panel';
import { DeviceService } from '#services/device-service';
import { ChangeDetectorRef, Component } from '@angular/core';

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
      setTimeout(() => {
        this.lastScan = date;
        this.cdr.detectChanges();
      });
    });
  }

  toggleViewMode(isLiveView: boolean) {
    this.deviceService.setAutoRefresh(isLiveView);
  }
}
