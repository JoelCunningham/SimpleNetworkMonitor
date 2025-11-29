import { Notification } from '#components/common';
import { Notification as NotificationDetails } from '#interfaces';
import { Component, Input } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-base-panel',
  imports: [Notification],
  templateUrl: './base-panel.html',
  styleUrl: './base-panel.scss',
})
export class BasePanel {
  @Input() panelTitle: string | null = null;
  @Input() notification?: NotificationDetails | null = null;
}
