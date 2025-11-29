import { Device, DeviceRequest } from '#interfaces';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, interval, Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({ providedIn: 'root' })
export class DeviceService {
  private apiUrl = 'http://192.168.0.15:8000/api/devices';
  private doRefresh = true;

  private devicesSubject = new BehaviorSubject<Device[]>([]);
  private lastRefreshSubject = new BehaviorSubject<Date | null>(null);

  public devices = this.devicesSubject.asObservable();
  public lastRefresh = this.lastRefreshSubject.asObservable();

  constructor(private http: HttpClient) {
    this.refreshDevices();

    interval(60000).subscribe(() => {
      if (this.doRefresh) {
        this.refreshDevices();
      }
    });
  }

  refreshDevices(): void {
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
      tap((newDevice) => {
        this.mergeDevices(newDevice);
      })
    );
  }

  updateDevice(id: number, device: DeviceRequest): Observable<Device> {
    return this.http.put<Device>(`${this.apiUrl}/${id}`, device).pipe(
      tap((updatedDevice) => {
        this.mergeDevices(updatedDevice);
      })
    );
  }

  deleteDevice(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        this.removeDevice(id);
      })
    );
  }

  mergeDevices(device: Device): void {
    const currentDevices = [...this.devicesSubject.value];

    const index = currentDevices.findIndex((d) => d.id === device.id);
    if (index !== -1) {
      currentDevices[index] = device;
    } else {
      currentDevices.push(device);
    }

    this.devicesSubject.next(currentDevices);
  }

  removeDevice(id: number): void {
    const current = [...this.devicesSubject.value];
    const filtered = current.filter((d) => d.id !== id);
    this.devicesSubject.next(filtered);
  }

  removeOwnerFromDevices(id: number): void {
    const current = [...this.devicesSubject.value];

    const updated = current.map((d) => {
      if (d.owner && d.owner.id === id) {
        return { ...d, owner: null } as Device;
      }
      return d;
    });

    if (updated !== current) {
      this.devicesSubject.next(updated);
    }
  }

  setAutoRefresh(enabled: boolean): void {
    this.doRefresh = enabled;
    if (enabled) {
      this.refreshDevices();
    }
  }
}
