import { Environment } from '#environment';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { DeviceService } from './device-service';

describe('DeviceService', () => {
  let service: DeviceService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [DeviceService],
    });
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    service = TestBed.inject(DeviceService);

    // Handle the initial HTTP request made by the constructor
    const req = httpMock.expectOne(`${Environment.apiUrl}/devices`);
    req.flush([]);

    expect(service).toBeTruthy();
  });
});
