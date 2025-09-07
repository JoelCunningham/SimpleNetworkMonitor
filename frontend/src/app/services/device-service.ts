import { Device } from '#interfaces/device';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, interval, Observable, Subscription } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class DeviceService {
  private apiUrl = 'http://localhost:5000/api/devices';
  private devicesSubject = new BehaviorSubject<Device[]>([]);

  public devices = this.devicesSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadDevices();

    interval(60000).subscribe(() => {
      this.loadDevices();
      console.log('Devices updated');
    });
  }

  private loadDevices(): void {
    this.http.get<Device[]>(this.apiUrl).subscribe((devices) => {
      this.devicesSubject.next(devices);
    });
  }

  currentDevices(): Observable<Device[]> {
    return this.devices;
  }

  createDevice(device: Device): Observable<Device> {
    return this.http.post<Device>(this.apiUrl, device);
  }

  updateDevice(device: Device): Observable<Device> {
    return this.http.put<Device>(`${this.apiUrl}/${device.id}`, device);
  }

  deleteDevice(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`);
  }

  refreshDevices(): void {
    this.loadDevices();
  }
}
