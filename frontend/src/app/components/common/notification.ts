import { Icon } from '#components/common/icon';
import { NotificationType } from '#types';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-notification',
  imports: [Icon],
  templateUrl: './notification.html',
  styleUrl: './notification.scss',
})
export class Notification {
  @Input() message: string | null = null;
  @Input() type: NotificationType | null = null;
  @Input() css: string = '';
  @Input() closeable: boolean = true;
  @Output() onClose = new EventEmitter<void>();

  protected visible: boolean = false;

  ngOnChanges() {
    const hasType = this.type !== null;
    const hasMessage = this.message !== null && this.message.trim() !== '';
    this.visible = hasMessage && hasType;
  }

  closeNotification() {
    this.onClose.emit();
  }
}
