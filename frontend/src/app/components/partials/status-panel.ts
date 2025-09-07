import { Icon } from '#components/common/icon';
import { Component } from '@angular/core';

@Component({
  selector: 'app-status-panel',
  imports: [Icon],
  templateUrl: './status-panel.html',
  styleUrl: './status-panel.scss',
})
export class StatusPanel {
  isLiveView = true;

  toggleViewMode() {
    this.isLiveView = !this.isLiveView;
  }
}
