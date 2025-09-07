import { Icon } from '#components/common/icon';
import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-form-section',
  imports: [Icon],
  templateUrl: './form-section.html',
  styleUrl: './form-section.scss',
})
export class FormSection {
  @Input() title: string = '';
  @Input() collapsible: boolean = false;

  protected collapsed: boolean = false;

  toggle() {
    if (this.collapsible) {
      this.collapsed = !this.collapsed;
    }
  }
}
