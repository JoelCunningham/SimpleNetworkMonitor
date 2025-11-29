import {
  DevicesPanel,
  OwnersPanel,
  StatusPanel,
  UnknownDevicesPanel,
} from '#components/panels';
import { Header } from '#components/partials';
import { Component, signal } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-root',
  imports: [
    Header,
    DevicesPanel,
    OwnersPanel,
    StatusPanel,
    UnknownDevicesPanel,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App {
  protected readonly title = signal('frontend');
}
