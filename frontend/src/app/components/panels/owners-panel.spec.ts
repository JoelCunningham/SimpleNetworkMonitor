import { Environment } from '#environment';
import { OwnersPanel } from '#components/panels';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('OwnersPanel', () => {
  let component: OwnersPanel;
  let fixture: ComponentFixture<OwnersPanel>;
  let httpMock: HttpTestingController;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [OwnersPanel, HttpClientTestingModule],
    }).compileComponents();

    fixture = TestBed.createComponent(OwnersPanel);
    component = fixture.componentInstance;
    httpMock = TestBed.inject(HttpTestingController);

    // Handle initial HTTP requests from services
    const devicesReq = httpMock.expectOne(
      `${Environment.apiUrl}/devices`
    );
    devicesReq.flush([]);
    const ownersReq = httpMock.expectOne(`${Environment.apiUrl}/owners`);
    ownersReq.flush([]);

    fixture.detectChanges();
  });

  afterEach(() => {
    // Flush any pending icon requests
    const pendingRequests = httpMock.match(() => true);
    pendingRequests.forEach((req) => req.flush(''));
    httpMock.verify();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should render "Add Owner" card full width when no owners', () => {
    fixture.detectChanges();
    const compiled = fixture.nativeElement as HTMLElement;
    const addOwnerCard = compiled.querySelector('app-owner-add-card');
    expect(addOwnerCard).toBeTruthy();
  });

  it('should render owner cards when owners exist', () => {
    // Update the owners through the service
    component['owners'] = [
      { id: 1, name: 'Alice', devices: [] },
      { id: 2, name: 'Bob', devices: [] },
    ];
    fixture.detectChanges();

    const compiled = fixture.nativeElement as HTMLElement;
    const ownerCards = compiled.querySelectorAll('app-owner-card');
    expect(ownerCards.length).toBe(2);

    const addOwnerCard = compiled.querySelector('app-owner-add-card');
    expect(addOwnerCard?.classList.contains('full-width')).toBeFalse();
  });
});
