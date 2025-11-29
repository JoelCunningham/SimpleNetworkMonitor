import { Icon } from '#components/common';
import { Notification as NotificationDetails } from '#interfaces';
import {
  Component,
  ElementRef,
  EventEmitter,
  Input,
  Output,
} from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-notification',
  imports: [Icon],
  templateUrl: './notification.html',
  styleUrl: './notification.scss',
})
export class Notification {
  @Input() details?: NotificationDetails;
  @Input() closeable: boolean = true;

  @Output() onClose = new EventEmitter<void>();

  constructor(private ref: ElementRef) {}

  ngOnChanges() {
    this.ref.nativeElement.scrollIntoView({
      behavior: 'smooth',
      block: 'nearest',
    });
  }

  closeNotification() {
    this.onClose.emit();
  }
}
