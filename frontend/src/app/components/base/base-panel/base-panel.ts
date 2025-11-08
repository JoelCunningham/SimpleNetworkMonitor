import { Component, Input } from '@angular/core';
import { Notification } from '#components/common/notification';

@Component({
  selector: 'app-base-panel',
  imports: [Notification],
  templateUrl: './base-panel.html',
  styleUrl: './base-panel.scss',
})
export class BasePanel {
  @Input() title: string | null = null;

  public notification: Notification | null = null;
}
