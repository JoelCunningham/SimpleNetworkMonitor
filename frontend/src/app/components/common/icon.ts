import { IconService } from '#services';
import { CommonModule } from '@angular/common';
import { Component, Input, OnChanges, OnInit } from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { Observable, of } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-icon',
  imports: [CommonModule],
  templateUrl: './icon.html',
  styleUrl: './icon.scss',
})
export class Icon implements OnInit, OnChanges {
  @Input() name: string | null = null;
  @Input() type: string = 'icon';
  @Input() size: string = '';

  iconContent$: Observable<SafeHtml | null> = of(null);

  constructor(private iconService: IconService) {}

  ngOnInit() {
    this.loadIcon();
  }

  ngOnChanges() {
    this.loadIcon();
  }

  private loadIcon() {
    if (this.name) {
      this.iconContent$ = this.iconService.loadIcon(this.name, this.type);
    }
  }
}
