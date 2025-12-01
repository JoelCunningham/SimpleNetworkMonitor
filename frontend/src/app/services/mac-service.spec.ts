import { Environment } from '#environment';
import { MacService } from '#services';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

describe('MacService', () => {
  let service: MacService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [MacService],
    });
    service = TestBed.inject(MacService);
    httpMock = TestBed.inject(HttpTestingController);

    // Handle the initial HTTP request made by the constructor
    const req = httpMock.expectOne(`${Environment.apiUrl}/macs`);
    req.flush([]);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
