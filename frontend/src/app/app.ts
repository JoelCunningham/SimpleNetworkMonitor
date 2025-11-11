import { OwnersPanel } from '#components/owners-panel/owners-panel';
import { DevicesPanel } from '#components/partials/devices-panel';
import { Header } from '#components/partials/header';
import { StatusPanel } from '#components/status-panel/status-panel';
import { Component, signal } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [Header, DevicesPanel, OwnersPanel, StatusPanel],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('frontend');
}
