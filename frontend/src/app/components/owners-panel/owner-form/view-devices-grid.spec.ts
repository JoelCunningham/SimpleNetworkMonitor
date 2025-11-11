import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewDevicesGrid } from './view-devices-grid';

describe('ViewDevicesGrid', () => {
  let component: ViewDevicesGrid;
  let fixture: ComponentFixture<ViewDevicesGrid>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ViewDevicesGrid]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ViewDevicesGrid);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
