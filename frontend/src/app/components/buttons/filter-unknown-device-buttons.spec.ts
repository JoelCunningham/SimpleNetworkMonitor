import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FilterUnknownDeviceButtons } from './filter-unknown-device-buttons';

describe('FilterUnknownDeviceButtons', () => {
  let component: FilterUnknownDeviceButtons;
  let fixture: ComponentFixture<FilterUnknownDeviceButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FilterUnknownDeviceButtons]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FilterUnknownDeviceButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
