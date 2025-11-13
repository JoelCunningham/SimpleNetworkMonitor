import { LiveViewButton } from '#components/buttons';
import { LastScanText } from '#components/fields';
import { BasePanel } from '#components/panels';
import { DeviceService } from '#services';
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
