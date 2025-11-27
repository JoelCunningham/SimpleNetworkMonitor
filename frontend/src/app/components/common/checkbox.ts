import { Icon } from '#/components/common/icon';
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
    this.checkedChange.emit(!this.checked);
  }
}
