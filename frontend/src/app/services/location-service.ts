import { Location } from '#interfaces/location';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class LocationService {
  private apiUrl = 'http://localhost:5000/api/locations';
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
