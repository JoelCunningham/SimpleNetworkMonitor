import { MacService } from '#services/mac-service';
import { TestBed } from '@angular/core/testing';

describe('MacService', () => {
  let service: MacService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MacService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
