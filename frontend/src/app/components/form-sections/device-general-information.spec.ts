import { DeviceGeneralInformation } from '#components/form-sections';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DeviceGeneralInformation', () => {
  let component: DeviceGeneralInformation;
  let fixture: ComponentFixture<DeviceGeneralInformation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceGeneralInformation],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceGeneralInformation);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
