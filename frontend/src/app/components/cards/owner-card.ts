import { BaseCard } from '#components/cards/base-card';
import { Owner } from '#interfaces/owner';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-owner-card',
  imports: [BaseCard],
  templateUrl: './owner-card.html',
  styleUrl: './owner-card.scss',
})
export class OwnerCard {
  @Input() owner!: Owner;
  @Output() onClick = new EventEmitter<Owner>();

  click(owner: Owner) {
    this.onClick.emit(owner);
  }
}
