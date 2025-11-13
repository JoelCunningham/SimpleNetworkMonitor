import { DeviceCard } from '#components/cards/device-card';
import { Owner } from '#interfaces/owner';
import { Component, Input } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-view-devices-grid',
  imports: [DeviceCard],
  templateUrl: './view-devices-grid.html',
  styleUrl: './view-devices-grid.scss',
})
export class ViewDevicesGrid {
  @Input() owner!: Owner;
}
