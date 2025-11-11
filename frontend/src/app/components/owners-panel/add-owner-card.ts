import { BaseCard } from '#components/base/base-card';
import { Icon } from '#components/common/icon';
import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-add-owner-card',
  imports: [BaseCard, Icon],
  templateUrl: './add-owner-card.html',
  styleUrl: './add-owner-card.scss',
})
export class AddOwnerCard {
  @Output() onClick = new EventEmitter<void>();

  click() {
    this.onClick.emit();
  }
}
