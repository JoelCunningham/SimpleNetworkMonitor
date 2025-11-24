import { Icon } from '#components/common';
import { Component, Input } from '@angular/core';

@Component({
  standalone: true,
  selector: 'app-base-form-section',
  imports: [Icon],
  templateUrl: './base-form-section.html',
  styleUrl: './base-form-section.scss',
})
export class BaseFormSection {
  @Input() sectionTitle: string = '';
  @Input() collapsible: boolean = false;

  protected collapsed: boolean = false;

  toggle() {
    if (this.collapsible) {
      this.collapsed = !this.collapsed;
    }
  }
}
