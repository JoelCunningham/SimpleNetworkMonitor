import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { DomSanitizer, SafeHtml } from '@angular/platform-browser';
import { catchError, map, Observable, of, shareReplay } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class IconService {
  private cache = new Map<string, Observable<SafeHtml | null>>();

  constructor(private http: HttpClient, private sanitizer: DomSanitizer) {}

  loadIcon(name: string, type: string): Observable<SafeHtml | null> {
    const cacheKey = `${type}-${name}`;

    if (this.cache.has(cacheKey)) {
      return this.cache.get(cacheKey)!;
    }

    const icon = this.http
      .get(`/${type}s/${name}.svg`, { responseType: 'text' })
      .pipe(
        map((icon) => this.sanitizer.bypassSecurityTrustHtml(icon)),
        catchError(() => of(null)),
        shareReplay(1)
      );

    this.cache.set(cacheKey, icon);
    return icon;
  }
}
