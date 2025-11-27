import { Component, Input, Output, EventEmitter } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-edit-field',
  imports: [FormsModule],
  templateUrl: './edit-field.html',
  styleUrl: './edit-field.scss',
})
export class EditField {
  @Input() label: string = '';
  @Input() value: string | null = null;
  @Input() placeholder: string = '';
  @Input() hasError: boolean = false;
  @Input() disabled: boolean = false;

  @Output() valueChange = new EventEmitter<string | null>();

  clearError() {
    this.hasError = false;
  }

  onValueChange(value: string | null) {
    this.value = value;
    this.clearError();
    this.valueChange.emit(value);
  }
}
