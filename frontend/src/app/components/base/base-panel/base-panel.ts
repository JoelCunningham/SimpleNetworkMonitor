import { Notification as AppNotification } from '#components/common/notification';
import { Notification } from '#interfaces/notification';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-base-panel',
  imports: [AppNotification],
  templateUrl: './base-panel.html',
  styleUrl: './base-panel.scss',
})
export class BasePanel {
  @Input() title: string | null = null;
  @Input() notification: Notification | null = null;
}
