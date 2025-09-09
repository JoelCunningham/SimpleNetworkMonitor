import { Owner } from '#interfaces/owner';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable, tap } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class OwnerService {
  private apiUrl = 'http://localhost:8000/api/owners';
  private ownersSubject = new BehaviorSubject<Owner[]>([]);

  public owners = this.ownersSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadOwners();
  }

  private loadOwners(): void {
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

  createOwner(owner: Owner): Observable<Owner> {
    const request: OwnerRequest = {
      name: owner.name,
      device_ids: owner.devices.map((device) => device.id),
    };

    return this.http.post<Owner>(this.apiUrl, request).pipe(
      tap((newOwner) => {
        const currentOwners = this.ownersSubject.value;
        this.ownersSubject.next([...currentOwners, newOwner]);
      })
    );
  }

  updateOwner(owner: Owner): Observable<Owner> {
    const request: OwnerRequest = {
      name: owner.name,
      device_ids: owner.devices.map((device) => device.id),
    };

    return this.http.put<Owner>(`${this.apiUrl}/${owner.id}`, request).pipe(
      tap((updatedOwner) => {
        const currentOwners = this.ownersSubject.value;
        const index = currentOwners.findIndex((o) => o.id === owner.id);
        if (index !== -1) {
          const newOwners = [...currentOwners];
          newOwners[index] = updatedOwner;
          this.ownersSubject.next(newOwners);
        }
      })
    );
  }

  deleteOwner(ownerId: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/${ownerId}`).pipe(
      tap(() => {
        const currentOwners = this.ownersSubject.value;
        const filteredOwners = currentOwners.filter((o) => o.id !== ownerId);
        this.ownersSubject.next(filteredOwners);
      })
    );
  }

  refreshOwners(): void {
    this.loadOwners();
  }
}

interface OwnerRequest {
  name: string;
  device_ids: number[];
}
