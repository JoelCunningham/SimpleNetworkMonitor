import { Icon } from '#components/common/icon';
import {
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  Input,
  Output,
} from '@angular/core';

@Component({
  selector: 'app-modal',
  imports: [Icon],
  templateUrl: './modal.html',
  styleUrl: './modal.scss',
})
export class Modal {
  @Input() title: string | null = '';
  @Input() isOpen: boolean = false;
  @Output() onClose = new EventEmitter<void>();

  constructor(private el: ElementRef) {}

  closeModal() {
    this.onClose.emit();
  }

  @HostListener('document:keydown.escape', ['$event'])
  handleEscape(event: Event) {
    if (this.isOpen) {
      this.closeModal();
    }
  }

  onBackgroundClick(event: MouseEvent) {
    if (
      this.isOpen &&
      event.target === this.el.nativeElement.querySelector('.modal')
    ) {
      this.closeModal();
    }
  }
}
