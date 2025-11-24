import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditDeviceButtons } from './edit-device-buttons';

describe('EditDeviceButtons', () => {
  let component: EditDeviceButtons;
  let fixture: ComponentFixture<EditDeviceButtons>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditDeviceButtons]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditDeviceButtons);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
