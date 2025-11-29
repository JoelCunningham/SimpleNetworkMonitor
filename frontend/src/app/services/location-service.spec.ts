import { LocationService } from '#services';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

describe('LocationService', () => {
  let service: LocationService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [LocationService],
    });
    service = TestBed.inject(LocationService);
    httpMock = TestBed.inject(HttpTestingController);

    // Handle the initial HTTP request made by the constructor
    const req = httpMock.expectOne('http://192.168.0.15:8000/api/locations');
    req.flush([]);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
