import { provideHttpClient } from '@angular/common/http';
import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterDeviceButtons } from './filter-device-buttons';

describe('FilterDeviceButtons', () => {
  let component: FilterDeviceButtons;
  let fixture: ComponentFixture<FilterDeviceButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FilterDeviceButtons],
      providers: [provideHttpClient()],
    }).compileComponents();

    fixture = TestBed.createComponent(FilterDeviceButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
