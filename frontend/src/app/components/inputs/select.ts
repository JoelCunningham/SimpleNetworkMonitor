import { Icon } from '#components/common/icon';
import { Option, Value } from '#interfaces/option';
import {
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  Input,
  OnChanges,
  Output,
} from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-select',
  imports: [Icon],
  templateUrl: './select.html',
  styleUrl: './select.scss',
})
export class Select implements OnChanges {
  @Input() css?: string;
  @Input() options: Option[] = [];
  @Input() placeholder?: string;
  @Input() initialOption?: Option;
  @Input() isClearable: boolean = false;
  @Input() isPersistent: boolean = false;

  @Output() optionSelected = new EventEmitter<Value>();

  protected isOpen = false;
  protected selectText: string = 'Select...';
  protected selectOptions: Option[] = [];

  constructor(private ref: ElementRef) {}

  ngOnChanges() {
    this.selectOptions = this.options.map((option) => ({
      ...option,
      event: this.selectOption.bind(this, option),
    }));

    if (this.isClearable) {
      this.selectOptions.push({
        label: 'Clear',
        value: 0,
        event: this.clearSelection.bind(this),
      });
    }

    if (this.initialOption) {
      this.selectText = this.initialOption.label;
    } else if (this.placeholder) {
      this.selectText = this.placeholder;
    } else {
      this.selectText = 'Select...';
    }
  }

  toggleDropdown() {
    if (!this.isDisabled()) {
      this.isOpen = !this.isOpen;
    }
  }

  selectOption(option: Option) {
    this.optionSelected.emit(option.value);
    this.isOpen = false;

    if (this.isPersistent) {
      this.selectText = option.label;
    }
  }

  clearSelection() {
    this.optionSelected.emit(null);
    this.isOpen = false;
    this.selectText = this.placeholder || 'Select...';
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
