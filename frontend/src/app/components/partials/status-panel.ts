import { BasePanel } from '#components/base/base-panel';
import { Icon } from '#components/common/icon';
import { DeviceService } from '#services/device-service';
import { DatePipe } from '@angular/common';
import { ChangeDetectorRef, Component } from '@angular/core';

@Component({
  selector: 'app-status-panel',
  imports: [BasePanel, Icon, DatePipe],
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
      setTimeout(() => {
        this.lastScan = date;
        this.cdr.detectChanges();
      });
    });
  }

  toggleViewMode() {
    this.isLiveView = !this.isLiveView;
    this.deviceService.setAutoRefresh(this.isLiveView);
  }
}
