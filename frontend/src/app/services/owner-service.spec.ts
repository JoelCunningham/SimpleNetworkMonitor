import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { Owner } from '#interfaces/owner';
import { OwnerService } from '#services/owner-service';

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

    service.getAllOwners().subscribe((owners) => {
      expect(owners.length).toBe(2);
      expect(owners).toEqual(mockOwners);
    });

    const req = httpMock.expectOne('http://localhost:8000/api/owners');
    expect(req.request.method).toBe('GET');
    req.flush(mockOwners);
  });
});
