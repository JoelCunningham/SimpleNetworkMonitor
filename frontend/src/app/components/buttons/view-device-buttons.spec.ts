import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewDeviceButtons } from './view-device-buttons';

describe('ViewDeviceButtons', () => {
  let component: ViewDeviceButtons;
  let fixture: ComponentFixture<ViewDeviceButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewDeviceButtons]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewDeviceButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
