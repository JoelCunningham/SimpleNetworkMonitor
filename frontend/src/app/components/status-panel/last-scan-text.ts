import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-last-scan-text',
  imports: [],
  templateUrl: './last-scan-text.html',
  styleUrl: './last-scan-text.scss',
})
export class LastScanText {
  @Input() lastScan: Date | null = null;

  lastScanFormatted() {
    return this.lastScan ? new Date(this.lastScan).toLocaleString() : 'Never';
  }
}
