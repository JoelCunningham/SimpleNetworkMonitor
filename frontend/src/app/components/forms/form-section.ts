import { Icon } from '#components/common';
import { Component, Input } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-form-section',
  imports: [Icon],
  templateUrl: './form-section.html',
  styleUrl: './form-section.scss',
})
export class FormSection {
  @Input() sectionTitle: string = '';
  @Input() collapsible: boolean = false;

  protected collapsed: boolean = false;

  toggle() {
    if (this.collapsible) {
      this.collapsed = !this.collapsed;
    }
  }
}
