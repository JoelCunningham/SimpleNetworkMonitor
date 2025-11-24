import { ViewField } from '#components/fields';
import { BaseFormSection } from '#components/form-sections';
import { Mac } from '#interfaces';
import { DatePipe } from '@angular/common';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-device-network-information',
  imports: [BaseFormSection, ViewField, DatePipe],
  templateUrl: './device-network-information.html',
  styleUrl: './device-network-information.scss',
})
export class DeviceNetworkInformation {
  @Input() mac!: Mac;
}
