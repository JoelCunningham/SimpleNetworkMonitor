import { Icon } from '#components/common/icon';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-base-card',
  imports: [Icon],
  templateUrl: './base-card.html',
  styleUrl: './base-card.scss',
})
export class BaseCard<T> {
  @Input() title: string | null = null;
  @Input() value: T | null = null;

  @Input() primary: boolean = false;
  @Input() selected: boolean = false;
  @Input() removable: boolean = false;
  @Input() interactive: boolean = true;

  @Input() fullWidth: boolean = false;

  @Output() onClick = new EventEmitter<T | null>();
  @Output() onRemove = new EventEmitter<T | null>();

  click() {
    this.onClick.emit(this.value);
  }

  remove() {
    this.onRemove.emit(this.value);
  }
}
