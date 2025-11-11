import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-field-view',
  imports: [],
  templateUrl: './field-view.html',
  styleUrl: './field-view.scss',
})
export class FieldView {
  @Input() label: string = '';
  @Input() value: string = '';
}
