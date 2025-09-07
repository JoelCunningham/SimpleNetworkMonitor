import { Icon } from '#components/common/icon';
import { Option, Value } from '#interfaces/option';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-basic-card',
  imports: [Icon],
  templateUrl: './basic-card.html',
  styleUrl: './basic-card.scss',
})
export class BasicCard {
  @Input() data: Option | null = null;
  @Input() addText: string = '';
  @Input() selected: boolean = false;
  @Input() badgeText: string | null = null;
  @Input() padding: string = '1rem';
  @Input() fullWidth: Boolean = false;
  @Input() showRemove: boolean = false;

  @Output() onClick = new EventEmitter<Value | null>();
  @Output() onRemove = new EventEmitter<Value | null>();

  handleClick() {
    this.onClick.emit(this.data?.value);
  }
}
