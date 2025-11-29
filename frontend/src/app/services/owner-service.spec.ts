import { Owner } from '#interfaces';
import { OwnerService } from '#services';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

describe('OwnerService', () => {
  let service: OwnerService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [OwnerService],
    });
    service = TestBed.inject(OwnerService);
    httpMock = TestBed.inject(HttpTestingController);

    // Handle the initial HTTP requests made by OwnerService and DeviceService constructors
    const devicesReq = httpMock.expectOne(
      'http://192.168.0.15:8000/api/devices'
    );
    devicesReq.flush([]);
    const ownersReq = httpMock.expectOne('http://192.168.0.15:8000/api/owners');
    ownersReq.flush([]);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should fetch all owners', () => {
    const mockOwners: Owner[] = [
      { id: 1, name: 'Alice', devices: [] },
      { id: 2, name: 'Bob', devices: [] },
    ];

    // Manually trigger a refresh to test the HTTP call
    service.refreshOwners();

    const req = httpMock.expectOne('http://192.168.0.15:8000/api/owners');
    expect(req.request.method).toBe('GET');
    req.flush(mockOwners);

    // Verify the owners were updated
    service.currentOwners().subscribe((owners) => {
      expect(owners.length).toBe(2);
      expect(owners).toEqual(mockOwners);
    });
  });
});
