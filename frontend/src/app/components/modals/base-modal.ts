import { Icon, Notification } from '#components/common';
import { Notification as NotificationDetails } from '#interfaces';
import {
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  Input,
  Output,
} from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-base-modal',
  imports: [Icon, Notification],
  templateUrl: './base-modal.html',
  styleUrl: './base-modal.scss',
})
export class BaseModal {
  @Input() isOpen: boolean = false;
  @Input() modalTitle!: string;
  @Input() notification?: NotificationDetails;

  @Output() onClose = new EventEmitter<void>();

  constructor(private ref: ElementRef) {}

  closeModal() {
    this.onClose.emit();
  }

  closeNotification() {
    this.notification = undefined;
  }

  @HostListener('document:keydown.escape', ['$event'])
  handleEscape(event: Event) {
    if (this.isOpen) {
      this.closeModal();
    }
  }
  @HostListener('document:click', ['$event'])
  onBackgroundClick(event: MouseEvent) {
    if (
      this.isOpen &&
      event.target === this.ref.nativeElement.querySelector('.modal')
    ) {
      this.closeModal();
    }
  }
}
