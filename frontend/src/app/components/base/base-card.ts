import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-base-card',
  templateUrl: './base-card.html',
  styleUrl: './base-card.scss',
})
export class BaseCard<T> {
  @Input() title: string | null = null;
  @Input() value: T | null = null;

  @Input() primary: boolean = false;
  @Input() selected: boolean = false;
  @Input() flexible: boolean = true;
  @Input() interactive: boolean = true;

  @Output() onClick = new EventEmitter<T | null>();

  click() {
    this.onClick.emit(this.value);
  }
}
