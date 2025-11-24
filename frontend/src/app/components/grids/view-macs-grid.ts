import { BaseCard } from '#components/cards';
import { Device, Mac } from '#interfaces';
import { Component, EventEmitter, Input, Output } from '@angular/core';

@Component({
  selector: 'app-view-macs-grid',
  imports: [BaseCard],
  templateUrl: './view-macs-grid.html',
  styleUrl: './view-macs-grid.scss',
})
export class ViewMacsGrid {
  @Input() device!: Device;
  @Input() currentMac!: Mac;

  @Output() onSelectMac = new EventEmitter<Mac>();

  select(mac: Mac) {
    this.onSelectMac.emit(mac);
  }

  getSortedMacs(device: Device): Mac[] {
    if (!device.macs) return [];
    return [...device.macs].sort((a, b) => {
      const aTime = a && a.last_seen ? new Date(a.last_seen).getTime() : 0;
      const bTime = b && b.last_seen ? new Date(b.last_seen).getTime() : 0;
      const aVal = isNaN(aTime) ? 0 : aTime;
      const bVal = isNaN(bTime) ? 0 : bTime;
      return bVal - aVal;
    });
  }
}
