import { Icon } from '#components/common';
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
  imports: [Icon],
  templateUrl: './base-modal.html',
  styleUrl: './base-modal.scss',
})
export class BaseModal {
  @Input() title: string | null = '';
  @Input() isOpen: boolean = false;
  @Output() onClose = new EventEmitter<void>();

  constructor(private ref: ElementRef) {}

  closeModal() {
    this.onClose.emit();
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
