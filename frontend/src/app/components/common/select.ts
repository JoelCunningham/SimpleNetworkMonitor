import { Icon } from '#components/common';
import { Option } from '#interfaces';
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
  selector: 'app-select',
  imports: [Icon],
  templateUrl: './select.html',
  styleUrl: './select.scss',
})
export class Select<T> {
  @Input() css?: string;
  @Input() options: Option<T>[] = [];
  @Input() selected?: Option<T> | null;
  @Input() placeholder?: string;
  @Input() isClearable: boolean = false;
  @Input() isPersistent: boolean = false;
  @Input() isReversed: boolean = false;

  @Output() selectedChange = new EventEmitter<Option<T> | null>();

  private defaultPlaceholder: string = 'Select...';

  protected isOpen = false;
  protected selectText: string = this.defaultPlaceholder;
  protected selectOptions: Option<T>[] = [];

  constructor(private ref: ElementRef) {}

  ngOnChanges() {
    this.selectOptions = this.options.map((option) => ({
      ...option,
      event: this.selectOption.bind(this, option),
    }));

    if (this.isClearable && this.selected) {
      this.selectOptions.push({
        label: 'Clear',
        event: this.clearSelection.bind(this),
      });
    }

    if (this.selected) {
      this.selectText = this.selected.label;
    } else if (this.placeholder) {
      this.selectText = this.placeholder;
    } else {
      this.selectText = this.defaultPlaceholder;
    }
  }

  toggleDropdown() {
    if (!this.isDisabled()) {
      this.isOpen = !this.isOpen;
    }
  }

  selectOption(option: Option<T>) {
    this.selectedChange.emit(option);
    this.isOpen = false;
    if (this.isPersistent) {
      this.selectText = option.label;
    }
  }

  clearSelection() {
    this.selectedChange.emit(null);
    this.isOpen = false;
    this.selectText = this.placeholder || this.defaultPlaceholder;
  }

  getDropdownHeight(): string {
    return this.selectOptions.length * 39 + 'px';
  }

  isDisabled(): boolean {
    return this.selectOptions.length === 0;
  }

  @HostListener('document:keydown.escape', ['$event'])
  handleEscape(event: Event) {
    if (this.isOpen) {
      this.isOpen = false;
    }
  }
  @HostListener('document:click', ['$event'])
  onBackgroundClick(event: MouseEvent) {
    if (this.isOpen && !this.ref.nativeElement.contains(event.target)) {
      this.isOpen = false;
    }
  }
}
