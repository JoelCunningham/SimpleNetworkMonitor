import { DevicesPanel } from '#components/panels/devices-panel';
import { Header } from '#components/panels/header';
import { OwnersPanel } from '#components/panels/owners-panel';
import { StatusPanel } from '#components/panels/status-panel';
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
