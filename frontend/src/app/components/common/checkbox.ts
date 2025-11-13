import { Icon } from '#components/common';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-checkbox',
  imports: [Icon],
  templateUrl: './checkbox.html',
  styleUrls: ['./checkbox.scss'],
})
export class Checkbox {
  @Input() label?: string;
  @Input() checked: boolean = false;

  @Output() checkedChange = new EventEmitter<boolean>();

  toggle() {
    this.checked = !this.checked;
    this.checkedChange.emit(this.checked);
  }
}
