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
  @Input() options: Option<T>[] = [];

  @Input() css?: string;
  @Input() placeholder?: string;
  @Input() isClearable: boolean = false;
  @Input() isPersistent: boolean = false;
  @Input() isReversed: boolean = false;

  @Output() optionsChange = new EventEmitter<Option<T>[]>();

  private defaultPlaceholder: string = 'Select...';

  protected isOpen = false;
  protected selectText: string = this.defaultPlaceholder;
  protected selectOptions: Option<T>[] = [];

  constructor(private ref: ElementRef) {}

  ngDoCheck() {
    this.selectOptions = this.options.map((option) => ({
      ...option,
      event: this.selectOption.bind(this, option),
    }));

    const selectedOption = this.options.find((option) => option.selected);

    if (this.isClearable && selectedOption) {
      this.selectOptions.push({
        label: 'Clear',
        event: this.clearSelection.bind(this),
      });
    }

    if (selectedOption) {
      this.selectText = selectedOption.label;
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
    this.options.map((option) => (option.selected = false));
    option.selected = true;
    this.optionsChange.emit(this.options);
    this.isOpen = false;
  }

  clearSelection() {
    this.options.map((option) => (option.selected = false));
    this.optionsChange.emit(this.options);
    this.isOpen = false;
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
