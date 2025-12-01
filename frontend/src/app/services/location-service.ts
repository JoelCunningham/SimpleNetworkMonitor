import { Environment } from '#environment';
import { Location } from '#interfaces';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class LocationService {
  private apiUrl = `${Environment.apiUrl}/locations`;
  private locationsSubject = new BehaviorSubject<Location[]>([]);

  public locations = this.locationsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadLocations();
  }

  private loadLocations(): void {
    this.http.get<Location[]>(this.apiUrl).subscribe((locations) => {
      this.locationsSubject.next(locations);
    });
  }

  currentLocations(): Observable<Location[]> {
    return this.locations;
  }

  refreshLocations(): void {
    this.loadLocations();
  }
}
