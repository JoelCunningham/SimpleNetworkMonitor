import { BaseCard } from '#components/cards';
import { Icon } from '#components/common';
import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-owner-add-card',
  imports: [BaseCard, Icon],
  templateUrl: './owner-add-card.html',
  styleUrl: './owner-add-card.scss',
})
export class OwnerAddCard {
  @Output() onClick = new EventEmitter<void>();

  click() {
    this.onClick.emit();
  }
}
