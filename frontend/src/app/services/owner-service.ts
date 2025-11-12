import { Owner, OwnerRequest } from '#interfaces/owner';
import { DeviceService } from '#services/device-service';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class OwnerService {
  private apiUrl = 'http://localhost:8000/api/owners';
  private ownersSubject = new BehaviorSubject<Owner[]>([]);

  public owners = this.ownersSubject.asObservable();

  constructor(private http: HttpClient, private deviceService: DeviceService) {
    this.refreshOwners();
  }

  refreshOwners(): void {
    this.http.get<Owner[]>(this.apiUrl).subscribe((owners) => {
      owners.forEach((owner) =>
        owner.devices.forEach((device) => (device.owner = owner))
      );
      this.ownersSubject.next(owners);
    });
  }

  currentOwners(): Observable<Owner[]> {
    return this.owners;
  }

  createOwner(owner: OwnerRequest): Observable<Owner> {
    return this.http.post<Owner>(this.apiUrl, owner).pipe(
      tap((newOwner) => {
        this.mergeOwners(newOwner);
      })
    );
  }

  updateOwner(id: number, owner: OwnerRequest): Observable<Owner> {
    return this.http.put<Owner>(`${this.apiUrl}/${id}`, owner).pipe(
      tap((updatedOwner) => {
        this.mergeOwners(updatedOwner);
      })
    );
  }

  deleteOwner(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${id}`).pipe(
      tap(() => {
        this.removeOwner(id);
      })
    );
  }

  private mergeOwners(owner: Owner): void {
    const currentOwners = [...this.ownersSubject.value];

    if (owner.devices) {
      owner.devices.forEach((device) => (device.owner = owner));
    }

    const index = currentOwners.findIndex((o) => o.id === owner.id);
    if (index !== -1) {
      currentOwners[index] = owner;
    } else {
      currentOwners.push(owner);
    }

    this.ownersSubject.next(currentOwners);

    if (owner.devices && owner.devices.length > 0) {
      owner.devices.forEach((device) =>
        this.deviceService.mergeDevices(device)
      );
    }
  }

  private removeOwner(ownerId: number): void {
    const currentOwners = [...this.ownersSubject.value];
    const filteredOwners = currentOwners.filter((o) => o.id !== ownerId);
    this.ownersSubject.next(filteredOwners);
    this.deviceService.removeOwnerFromDevices(ownerId);
  }
}
