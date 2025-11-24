import { ViewField } from '#components/fields';
import { Device } from '#interfaces';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-device-general-information',
  imports: [ViewField],
  templateUrl: './device-general-information.html',
  styleUrl: './device-general-information.scss',
})
export class DeviceGeneralInformation {
  @Input() device!: Device;
}
