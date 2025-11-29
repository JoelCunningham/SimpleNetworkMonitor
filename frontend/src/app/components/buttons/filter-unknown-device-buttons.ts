import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-filter-unknown-device-buttons',
  imports: [],
  templateUrl: './filter-unknown-device-buttons.html',
  styleUrl: './filter-unknown-device-buttons.scss',
})
export class FilterUnknownDeviceButtons {
  @Input() timeLimit!: number;

  @Output() onFilterChange = new EventEmitter<void>();
  @Output() timeLimitChange = new EventEmitter<number>();

  filterChange(event: Event) {
    this.timeLimitChange.emit(Number((event.target as HTMLInputElement).value));
    this.onFilterChange.emit();
  }
}
