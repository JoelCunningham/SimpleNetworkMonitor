import { Device, DeviceRequest } from '#interfaces/device';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, interval, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class DeviceService {
  private apiUrl = 'http://localhost:8000/api/devices';
  private doRefresh = true;

  private devicesSubject = new BehaviorSubject<Device[]>([]);
  private lastRefreshSubject = new BehaviorSubject<Date | null>(null);

  public devices = this.devicesSubject.asObservable();
  public lastRefresh = this.lastRefreshSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadDevices();

    interval(60000).subscribe(() => {
      if (this.doRefresh) {
        this.loadDevices();
      }
    });
  }

  private loadDevices(): void {
    this.http.get<Device[]>(this.apiUrl).subscribe({
      next: (devices) => {
        this.devicesSubject.next(devices);
        this.lastRefreshSubject.next(new Date());
      },
      error: (error) => {
        console.error('Failed to load devices:', error);
      },
    });
  }

  currentDevices(): Observable<Device[]> {
    return this.devices;
  }

  createDevice(device: DeviceRequest): Observable<Device> {
    return this.http.post<Device>(this.apiUrl, device).pipe(
      tap(() => {
        this.loadDevices();
      })
    );
  }

  updateDevice(id: number, device: DeviceRequest): Observable<Device> {
    return this.http.put<Device>(`${this.apiUrl}/${id}`, device).pipe(
      tap(() => {
        this.loadDevices();
      })
    );
  }

  deleteDevice(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        this.loadDevices();
      })
    );
  }

  setAutoRefresh(enabled: boolean): void {
    this.doRefresh = enabled;
    if (enabled) {
      this.loadDevices();
    }
  }
}
