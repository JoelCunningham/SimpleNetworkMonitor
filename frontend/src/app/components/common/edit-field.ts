import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-edit-field',
  imports: [FormsModule],
  templateUrl: './edit-field.html',
  styleUrl: './edit-field.scss',
})
export class EditField {
  @Input() label: string = '';
  @Input() value: string = '';
  @Input() placeholder: string = '';
  @Input() hasError: boolean = false;

  clearError() {
    this.hasError = false;
  }
}
