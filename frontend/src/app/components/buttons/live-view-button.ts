import { Icon } from '#components/common';
import { Component, EventEmitter, Output } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-live-view-button',
  imports: [Icon],
  templateUrl: './live-view-button.html',
  styleUrl: './live-view-button.scss',
})
export class LiveViewButton {
  @Output() onChange = new EventEmitter<boolean>();

  protected isLiveView = true;

  toggleViewMode() {
    this.isLiveView = !this.isLiveView;
    this.onChange.emit(this.isLiveView);
  }
}
