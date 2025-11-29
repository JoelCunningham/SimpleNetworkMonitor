import { Mac } from '#interfaces';
import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { BehaviorSubject, Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class MacService {
  private apiUrl = 'http://192.168.0.15:8000/api/macs';
  private macsSubject = new BehaviorSubject<Mac[]>([]);

  public macs = this.macsSubject.asObservable();

  constructor(private http: HttpClient) {
    this.loadMacs();
  }

  private loadMacs(): void {
    this.http.get<Mac[]>(this.apiUrl).subscribe((macs) => {
      this.macsSubject.next(macs);
    });
  }

  currentMacs(): Observable<Mac[]> {
    return this.macs;
  }

  refreshMacs(): void {
    this.loadMacs();
  }
}
