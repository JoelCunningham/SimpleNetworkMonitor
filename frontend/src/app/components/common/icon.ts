import { IconService } from '#services/icon-service';
import { CommonModule } from '@angular/common';
import { Component, Input, OnInit } from '@angular/core';
import { SafeHtml } from '@angular/platform-browser';
import { Observable, of } from 'rxjs';

@Component({
  standalone: true,
  selector: 'app-icon',
  imports: [CommonModule],
  templateUrl: './icon.html',
  styleUrl: './icon.scss',
})
export class Icon implements OnInit {
  @Input() name: string | null = null;
  @Input() type: string = 'icon';
  @Input() size: string = '';

  iconContent$: Observable<SafeHtml | null> = of(null);

  constructor(private iconService: IconService) {}

  ngOnInit() {
    if (this.name) {
      this.iconContent$ = this.iconService.loadIcon(this.name, this.type);
    }
  }
}
