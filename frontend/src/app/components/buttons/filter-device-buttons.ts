import { Select } from '#components/common';
import { Category, Location, Option, Owner } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-filter-device-buttons',
  imports: [Select],
  templateUrl: './filter-device-buttons.html',
  styleUrl: './filter-device-buttons.scss',
})
export class FilterDeviceButtons {
  @Input() owners: Option<Owner>[] = [];
  @Input() locations: Option<Location>[] = [];
  @Input() categories: Option<Category>[] = [];

  @Output() onFilterChange = new EventEmitter<void>();
  @Output() ownersChange = new EventEmitter<Option<Owner>[]>();
  @Output() locationsChange = new EventEmitter<Option<Location>[]>();
  @Output() categoriesChange = new EventEmitter<Option<Category>[]>();

  filterSelected() {
    return (
      this.owners.some((owner) => owner.selected) ||
      this.locations.some((location) => location.selected) ||
      this.categories.some((category) => category.selected)
    );
  }

  filterChange() {
    this.onFilterChange.emit();
  }

  clearFilters() {
    this.owners.forEach((owner) => (owner.selected = false));
    this.locations.forEach((location) => (location.selected = false));
    this.categories.forEach((category) => (category.selected = false));
    this.onFilterChange.emit();
  }
}
