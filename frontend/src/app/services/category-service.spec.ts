import { CategoryService } from '#/services/category-service';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

describe('CategoryService', () => {
  let service: CategoryService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [CategoryService],
    });
    service = TestBed.inject(CategoryService);
    httpMock = TestBed.inject(HttpTestingController);

    // Handle the initial HTTP request made by the constructor
    const req = httpMock.expectOne('http://192.168.0.15:8000/api/categories');
    req.flush([]);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
