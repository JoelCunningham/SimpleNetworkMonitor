import { Device, DeviceRequest } from '#interfaces/device';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, interval, Observable, Subscription } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class DeviceService {
  private apiUrl = 'http://localhost:5000/api/devices';
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
    this.http.get<Device[]>(this.apiUrl).subscribe((devices) => {
      this.devicesSubject.next(devices);
      this.lastRefreshSubject.next(new Date());
    });
  }

  currentDevices(): Observable<Device[]> {
    return this.devices;
  }

  createDevice(device: DeviceRequest): Observable<Device> {
    return this.http.post<Device>(this.apiUrl, device);
  }

  updateDevice(device: DeviceRequest): Observable<Device> {
    return this.http.put<Device>(`${this.apiUrl}/${device.id}`, device);
  }

  deleteDevice(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  setAutoRefresh(enabled: boolean): void {
    this.doRefresh = enabled;
    if (enabled) {
      this.loadDevices();
    }
  }
}
