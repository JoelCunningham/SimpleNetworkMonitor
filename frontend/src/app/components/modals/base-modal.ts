import { Icon, Notification } from '#components/common';
import { Notification as NotificationDetails } from '#interfaces';
import {
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  Input,
  OnChanges,
  Output,
  SimpleChanges,
} from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-base-modal',
  imports: [Icon, Notification],
  templateUrl: './base-modal.html',
  styleUrl: './base-modal.scss',
})
export class BaseModal implements OnChanges {
  @Input() isOpen: boolean = false;
  @Input() modalTitle!: string;
  @Input() notification?: NotificationDetails;

  @Output() onClose = new EventEmitter<void>();

  constructor(private ref: ElementRef) {}

  ngOnChanges(): void {
    if (this.isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
  }

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
