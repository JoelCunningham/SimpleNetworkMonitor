import { EditField } from '#components/common/edit-field';
import { Option, Value } from '#interfaces/option';
import { Owner } from '#interfaces/owner';
import { Component, EventEmitter, Input, Output } from '@angular/core';
import { EditButtons } from './edit-buttons';
import { EditDevicesGrid } from './edit-devices-grid';
import { Device } from '#interfaces/device';
import { AddButtons } from './add-buttons';

@Component({
  standalone: true,
  selector: 'app-add-owner-form',
  imports: [EditField, EditDevicesGrid, AddButtons],
  templateUrl: './add-owner-form.html',
  styleUrl: './add-owner-form.scss',
})
export class AddOwnerForm {
  @Input() owner!: Owner;
  @Input() devices: Device[] = []; //TODO remove
  @Input() availableDevices: Option[] = [];

  @Output() onAdd = new EventEmitter<void>();
  @Output() onCancel = new EventEmitter<void>();
  @Output() onSelectDevice = new EventEmitter<Value>();
  @Output() onRemoveDevice = new EventEmitter<Device | null>(); // TODO not null

  ngOnInit() {
    this.owner.devices = this.devices;
  }

  ngOnChanges() {
    this.owner.devices = this.devices;
  }

  add() {
    this.onAdd.emit();
  }

  cancel() {
    this.onCancel.emit();
  }

  selectDevice(deviceId: Value) {
    this.onSelectDevice.emit(deviceId);
  }

  removeDevice(device: Device | null) {
    this.onRemoveDevice.emit(device);
  }
}
