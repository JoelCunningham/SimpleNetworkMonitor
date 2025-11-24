import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-view-field',
  imports: [FormsModule],
  templateUrl: './view-field.html',
  styleUrl: './view-field.scss',
})
export class ViewField {
  @Input() label: string = '';
  @Input() value?: string | null = null;
  @Input() short: boolean = true;

  getValue(): string {
    return this.value || 'N/A';
  }
}
